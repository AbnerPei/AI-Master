from __future__ import annotations

import html
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STAGES: list[tuple[str, str]] = [
    ("validation", "输入校验"),
    ("audio_extraction", "音频提取"),
    ("transcript_generation", "文案提取"),
    ("transcript_cleanup", "文案清洗"),
    ("ai_distillation", "AI 整理"),
    ("output_writing", "结果落盘"),
]
STOPWORDS = {
    "我们",
    "你们",
    "他们",
    "然后",
    "因为",
    "所以",
    "这个",
    "那个",
    "已经",
    "就是",
    "可以",
    "如果",
    "但是",
    "一个",
    "一些",
    "没有",
    "不是",
    "需要",
    "自己",
    "进行",
    "以及",
    "还是",
    "时候",
    "这里",
    "那里",
    "一下",
    "比较",
    "现在",
    "视频",
    "内容",
    "文案",
    "蒸馏",
    "任务",
}


class StageError(RuntimeError):
    def __init__(self, stage_key: str, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.stage_key = stage_key
        self.details = details or {}


@dataclass
class JobState:
    job_id: str
    video_path: str
    output_dir: str
    status: str = "queued"
    stage_key: str = "queued"
    stage_label: str = "等待开始"
    stage_index: int = -1
    started_at: str = field(default_factory=lambda: now_iso())
    updated_at: str = field(default_factory=lambda: now_iso())
    finished_at: str = ""
    run_dir: str = ""
    result_files: list[dict[str, str]] = field(default_factory=list)
    preview_markdown: str = ""
    error: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    logs: list[dict[str, str]] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def set_run_dir(self, run_dir: str) -> None:
        with self._lock:
            self.run_dir = run_dir
            self.updated_at = now_iso()

    def set_stage(self, stage_key: str) -> None:
        labels = {key: label for key, label in STAGES}
        index_lookup = {key: idx for idx, (key, _label) in enumerate(STAGES)}
        with self._lock:
            self.stage_key = stage_key
            self.stage_label = labels.get(stage_key, stage_key)
            self.stage_index = index_lookup.get(stage_key, -1)
            self.status = "running"
            self.updated_at = now_iso()

    def append_log(self, message: str, level: str = "info") -> None:
        entry = {"timestamp": now_iso(), "level": level, "message": message}
        with self._lock:
            self.logs.append(entry)
            self.updated_at = entry["timestamp"]
            run_dir = self.run_dir
        if run_dir:
            log_path = Path(run_dir) / "job.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with log_path.open("a", encoding="utf-8") as handle:
                handle.write(f"{entry['timestamp']} [{level.upper()}] {message}\n")

    def complete(self, metadata: dict[str, Any], result_files: list[dict[str, str]], preview_markdown: str) -> None:
        with self._lock:
            self.status = "succeeded"
            self.metadata = metadata
            self.result_files = result_files
            self.preview_markdown = preview_markdown
            self.finished_at = now_iso()
            self.updated_at = self.finished_at

    def fail(self, stage_key: str, message: str, metadata: dict[str, Any], error_details: dict[str, Any] | None = None) -> None:
        labels = {key: label for key, label in STAGES}
        index_lookup = {key: idx for idx, (key, _label) in enumerate(STAGES)}
        payload = {"stage_key": stage_key, "stage_label": labels.get(stage_key, stage_key), "message": message}
        if error_details:
            payload["details"] = error_details
        with self._lock:
            self.status = "failed"
            self.stage_key = stage_key
            self.stage_label = labels.get(stage_key, stage_key)
            self.stage_index = index_lookup.get(stage_key, -1)
            self.error = payload
            self.metadata = metadata
            self.finished_at = now_iso()
            self.updated_at = self.finished_at

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            progress = []
            for index, (stage_key, stage_label) in enumerate(STAGES):
                if self.status == "succeeded":
                    stage_status = "succeeded"
                elif self.status == "failed" and stage_key == self.stage_key:
                    stage_status = "failed"
                elif self.stage_index > index:
                    stage_status = "succeeded"
                elif self.stage_index == index and self.status == "running":
                    stage_status = "running"
                else:
                    stage_status = "pending"
                progress.append({"key": stage_key, "label": stage_label, "status": stage_status})

            return {
                "job_id": self.job_id,
                "video_path": self.video_path,
                "output_dir": self.output_dir,
                "run_dir": self.run_dir,
                "status": self.status,
                "stage_key": self.stage_key,
                "stage_label": self.stage_label,
                "stage_index": self.stage_index,
                "started_at": self.started_at,
                "updated_at": self.updated_at,
                "finished_at": self.finished_at,
                "result_files": list(self.result_files),
                "preview_markdown": self.preview_markdown,
                "error": self.error,
                "metadata": self.metadata,
                "logs": list(self.logs),
                "progress": progress,
            }


def now_iso() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")


def safe_filename_part(value: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|\r\n\t]+", "_", value).strip(" ._")
    return cleaned or "unnamed"


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def find_sidecar_transcript(video_path: Path) -> tuple[Path | None, str]:
    for suffix in (".srt", ".vtt", ".txt", ".md"):
        candidate = video_path.with_suffix(suffix)
        if candidate.exists():
            return candidate, suffix
    return None, ""


def parse_sidecar_text(sidecar_path: Path) -> str:
    text = sidecar_path.read_text(encoding="utf-8", errors="ignore")
    if sidecar_path.suffix.lower() == ".srt":
        return normalize_subtitle_blocks(text)
    if sidecar_path.suffix.lower() == ".vtt":
        cleaned = re.sub(r"^WEBVTT\s*", "", text, flags=re.IGNORECASE)
        return normalize_subtitle_blocks(cleaned)
    return collapse_text(text)


def normalize_subtitle_blocks(text: str) -> str:
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            lines.append("")
            continue
        if re.fullmatch(r"\d+", line):
            continue
        if "-->" in line:
            continue
        line = re.sub(r"<[^>]+>", "", line)
        lines.append(line)
    return collapse_text("\n".join(lines))


def collapse_text(text: str) -> str:
    lines = []
    for raw_line in text.splitlines():
        cleaned = re.sub(r"\s+", " ", raw_line).strip()
        if cleaned:
            lines.append(cleaned)
    return "\n".join(lines).strip()


def clean_transcript_text(text: str) -> str:
    chunks: list[str] = []
    buffer: list[str] = []
    for raw_line in text.splitlines():
        line = re.sub(r"\s+", " ", raw_line).strip()
        if not line:
            continue
        buffer.append(line)
        if re.search(r"[。！？!?]$", line):
            chunks.append(" ".join(buffer))
            buffer = []
    if buffer:
        chunks.append(" ".join(buffer))
    if not chunks:
        return collapse_text(text)
    deduped: list[str] = []
    last_line = ""
    for line in chunks:
        if line != last_line:
            deduped.append(line)
        last_line = line
    return "\n\n".join(deduped).strip()


def extract_sentences(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []
    pieces = re.split(r"(?<=[。！？!?])\s*", normalized)
    sentences = [piece.strip() for piece in pieces if piece.strip()]
    if sentences:
        return sentences
    return [normalized]


def keyword_candidates(text: str, limit: int = 8) -> list[str]:
    candidates = re.findall(r"[\u4e00-\u9fffA-Za-z0-9]{2,}", text)
    counter: dict[str, int] = {}
    for token in candidates:
        if token in STOPWORDS:
            continue
        counter[token] = counter.get(token, 0) + 1
    ranked = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    return [token for token, _score in ranked[:limit]]


def build_openai_request(url: str, fields: dict[str, str], file_field: str, file_path: Path) -> tuple[bytes, dict[str, str]]:
    boundary = f"----CodexBoundary{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for key, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )
    chunks.extend(
        [
            f"--{boundary}\r\n".encode("utf-8"),
            f'Content-Disposition: form-data; name="{file_field}"; filename="{file_path.name}"\r\n'.encode("utf-8"),
            b"Content-Type: application/octet-stream\r\n\r\n",
            file_path.read_bytes(),
            b"\r\n",
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
    )
    data = b"".join(chunks)
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}", "Content-Length": str(len(data))}
    return data, headers


def transcribe_with_openai(audio_path: Path) -> tuple[str, dict[str, Any]]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return "", {"available": False, "reason": "`OPENAI_API_KEY` 未配置"}

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("LOCAL_VIDEO_WORKBENCH_TRANSCRIBE_MODEL", "whisper-1")
    payload, headers = build_openai_request(
        f"{base_url}/audio/transcriptions",
        {"model": model, "response_format": "json"},
        "file",
        audio_path,
    )
    headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(f"{base_url}/audio/transcriptions", data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        return "", {"available": True, "reason": f"`OpenAI` 转录失败：HTTP {exc.code}", "detail": detail}
    except Exception as exc:  # noqa: BLE001
        return "", {"available": True, "reason": f"`OpenAI` 转录失败：{exc}"}

    return body.get("text", "").strip(), {"available": True, "provider": "openai", "model": model}


def summarize_with_openai(text: str, title: str) -> tuple[str, dict[str, Any]]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return "", {"available": False, "reason": "`OPENAI_API_KEY` 未配置"}

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("LOCAL_VIDEO_WORKBENCH_SUMMARY_MODEL", "gpt-4o-mini")
    prompt = (
        "你是一个视频内容整理助手。请根据提供的转录文案，用中文输出一个结构化 Markdown，"
        "包含：`内容速览`、`关键要点`、`值得复查的原句`、`行动项或启发`。"
        "要求内容紧凑、可读、不要杜撰。"
    )
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"标题：{title}\n\n转录文案如下：\n{text}",
            },
        ],
        "temperature": 0.3,
    }
    data = json.dumps(body).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    request = urllib.request.Request(f"{base_url}/chat/completions", data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        return "", {"available": True, "reason": f"`OpenAI` 整理失败：HTTP {exc.code}", "detail": detail}
    except Exception as exc:  # noqa: BLE001
        return "", {"available": True, "reason": f"`OpenAI` 整理失败：{exc}"}

    message = payload["choices"][0]["message"]["content"].strip()
    return message, {"available": True, "provider": "openai", "model": model}


def transcribe_with_local_asr(audio_path: Path) -> tuple[str, dict[str, Any]]:
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except Exception as exc:  # noqa: BLE001
        return "", {"available": False, "reason": f"`faster_whisper` 不可用：{exc}"}

    model_name = os.getenv("LOCAL_VIDEO_WORKBENCH_WHISPER_MODEL", "small")
    compute_type = os.getenv("LOCAL_VIDEO_WORKBENCH_WHISPER_COMPUTE_TYPE", "int8")
    try:
        model = WhisperModel(model_name, compute_type=compute_type)
        segments, info = model.transcribe(str(audio_path), vad_filter=True)
        text = " ".join(segment.text.strip() for segment in segments if segment.text.strip()).strip()
    except Exception as exc:  # noqa: BLE001
        return "", {"available": True, "reason": f"本地 `ASR` 失败：{exc}", "model": model_name}

    return text, {
        "available": True,
        "provider": "local-asr",
        "model": model_name,
        "language": getattr(info, "language", ""),
        "language_probability": getattr(info, "language_probability", 0),
    }


def heuristic_distillation(title: str, cleaned_text: str) -> tuple[str, dict[str, Any]]:
    sentences = extract_sentences(cleaned_text)
    overview = sentences[0] if sentences else "当前没有足够文案可供整理。"
    key_points = sentences[:5] if sentences else ["暂无可提炼要点。"]
    keywords = keyword_candidates(cleaned_text)
    quote_lines = sentences[:3] if sentences else []
    keyword_line = "、".join(f"`{keyword}`" for keyword in keywords) if keywords else "暂无。"
    key_point_lines = "\n".join(f"- {line}" for line in key_points)
    quote_section = "\n".join(f"> {line}" for line in quote_lines) if quote_lines else "> 暂无可引用原句。"

    markdown = f"""## 内容速览

- 标题：`{title}`
- 蒸馏方式：`heuristic-fallback`
- 关键词：{keyword_line}
- 一句话总结：{overview}

## 关键要点

{key_point_lines}

## 值得复查的原句

{quote_section}

## 行动项或启发

- 先基于当前转录文案做结构化整理，后续如有更高质量字幕或云端整理结果，可覆盖更新这份蒸馏稿。
- 如果这段视频需要进入长期知识库，建议再补充人物、主题或项目上下文。
"""
    return markdown.strip(), {"provider": "heuristic-fallback", "available": True}


def markdown_frontmatter(title: str, tags: list[str]) -> str:
    tags_yaml = "\n".join(f"  - {tag}" for tag in tags)
    return f"""---
创建日期: {now_iso_with_colon()}
title: {title}
tags:
{tags_yaml}
---
"""


def now_iso_with_colon() -> str:
    stamp = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    return f"{stamp[:-2]}:{stamp[-2:]}"


def render_raw_transcript_markdown(video_path: Path, transcript_text: str, transcript_meta: dict[str, Any]) -> str:
    source = transcript_meta.get("source", "unknown")
    details = json.dumps(transcript_meta, ensure_ascii=False, indent=2)
    frontmatter = markdown_frontmatter(f"{video_path.stem} 原始转录", ["transcript", "raw"])
    body = f"""
# {video_path.stem} 原始转录

## 元信息

- 视频文件：`{video_path.name}`
- 转录来源：`{source}`

## 原始文案

```text
{transcript_text}
```

## 转录详情

```json
{details}
```
"""
    return frontmatter + "\n" + body.strip() + "\n"


def render_clean_transcript_markdown(video_path: Path, cleaned_text: str, transcript_meta: dict[str, Any]) -> str:
    frontmatter = markdown_frontmatter(f"{video_path.stem} 清洗转录", ["transcript", "clean"])
    body = f"""
# {video_path.stem} 清洗转录

## 来源说明

- 原始视频：`{video_path.name}`
- 清洗依据：基于已有转录做去噪、断句和基础结构化
- 上游来源：`{transcript_meta.get("source", "unknown")}`

## 清洗后文案

{cleaned_text}
"""
    return frontmatter + "\n" + body.strip() + "\n"


def render_distillation_markdown(video_path: Path, distillation_body: str, distillation_meta: dict[str, Any], transcript_meta: dict[str, Any]) -> str:
    frontmatter = markdown_frontmatter(f"{video_path.stem} 蒸馏整理", ["distillation", "video-note"])
    body = f"""
# {video_path.stem} 蒸馏整理

## 任务说明

- 视频文件：`{video_path.name}`
- 转录来源：`{transcript_meta.get("source", "unknown")}`
- 整理方式：`{distillation_meta.get("provider", "unknown")}`

{distillation_body}
"""
    return frontmatter + "\n" + body.strip() + "\n"


def ensure_output_writable(path: Path) -> None:
    if not path.exists():
        raise StageError("validation", f"输出目录不存在：`{path}`")
    if not path.is_dir():
        raise StageError("validation", f"输出路径不是目录：`{path}`")
    try:
        with tempfile.NamedTemporaryFile(dir=path, prefix=".write-test-", delete=True):
            pass
    except Exception as exc:  # noqa: BLE001
        raise StageError("validation", f"输出目录不可写：`{path}`", {"error": str(exc)}) from exc


def ffprobe_metadata(video_path: Path) -> dict[str, Any]:
    ffprobe_path = shutil.which("ffprobe")
    if not ffprobe_path:
        return {}
    result = subprocess.run(
        [ffprobe_path, "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(video_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}


def run_command(command: list[str], stage_key: str, cwd: Path | None = None) -> None:
    result = subprocess.run(command, capture_output=True, text=True, cwd=str(cwd) if cwd else None, check=False)
    if result.returncode != 0:
        raise StageError(
            stage_key,
            f"命令执行失败：`{' '.join(command)}`",
            {"stdout": result.stdout.strip(), "stderr": result.stderr.strip(), "returncode": result.returncode},
        )


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def summarize_metadata_preview(metadata: dict[str, Any]) -> str:
    if "distillation_preview" in metadata:
        return metadata["distillation_preview"]
    return ""


def run_job(job: JobState) -> None:
    started = time.monotonic()
    metadata: dict[str, Any] = {
        "job_id": job.job_id,
        "status": "running",
        "video_path": job.video_path,
        "output_dir": job.output_dir,
        "transcript": {
            "source": "unresolved",
            "available": False,
            "attempts": [],
        },
        "distillation": {
            "provider": "unresolved",
        },
        "artifacts": {},
    }
    current_stage = "validation"
    run_dir: Path | None = None
    raw_transcript_text = ""
    cleaned_text = ""
    try:
        job.set_stage("validation")
        job.append_log("开始校验输入参数。")
        video_path = Path(job.video_path).expanduser()
        output_dir = Path(job.output_dir).expanduser()
        if not video_path.exists():
            raise StageError("validation", f"视频文件不存在：`{video_path}`")
        if video_path.suffix.lower() != ".mp4":
            raise StageError("validation", f"当前只支持 `mp4`，收到：`{video_path.suffix or '无扩展名'}`")
        ensure_output_writable(output_dir)
        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            raise StageError("validation", "当前环境缺少 `ffmpeg`，无法执行音频提取。")
        metadata["tooling"] = {
            "ffmpeg": ffmpeg_path,
            "ffprobe": shutil.which("ffprobe") or "",
            "faster_whisper_available": can_import("faster_whisper"),
            "openai_key_available": bool(os.getenv("OPENAI_API_KEY", "").strip()),
        }
        stamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
        run_dir = output_dir / f"片语蒸馏台-{safe_filename_part(video_path.stem)}-{stamp}"
        run_dir.mkdir(parents=True, exist_ok=False)
        job.set_run_dir(str(run_dir))
        metadata["run_dir"] = str(run_dir)
        metadata["video_probe"] = ffprobe_metadata(video_path)
        job.append_log(f"任务目录已创建：`{run_dir}`")

        current_stage = "audio_extraction"
        job.set_stage(current_stage)
        audio_path = run_dir / "audio.wav"
        job.append_log("开始用 `ffmpeg` 提取单声道 `wav` 音频。")
        run_command(
            [
                ffmpeg_path,
                "-y",
                "-i",
                str(video_path),
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-ar",
                "16000",
                "-ac",
                "1",
                str(audio_path),
            ],
            current_stage,
        )
        metadata["artifacts"]["audio_path"] = str(audio_path)
        job.append_log(f"音频提取完成：`{audio_path.name}`")

        current_stage = "transcript_generation"
        job.set_stage(current_stage)
        sidecar_path, _suffix = find_sidecar_transcript(video_path)
        transcript_meta: dict[str, Any] = {
            "source": "unresolved",
            "available": False,
            "attempts": [],
        }
        if sidecar_path:
            job.append_log(f"发现同名字幕文件：`{sidecar_path.name}`，优先复用。")
            raw_transcript_text = parse_sidecar_text(sidecar_path)
            transcript_meta.update(
                {
                    "source": "sidecar-subtitle",
                    "available": bool(raw_transcript_text),
                    "sidecar_path": str(sidecar_path),
                }
            )
            transcript_meta["attempts"].append({"source": "sidecar-subtitle", "success": bool(raw_transcript_text)})

        if not raw_transcript_text:
            job.append_log("未找到可用字幕，尝试本地 `ASR`。")
            local_text, local_meta = transcribe_with_local_asr(audio_path)
            transcript_meta["attempts"].append({"source": "local-asr", **local_meta, "success": bool(local_text)})
            if local_text:
                raw_transcript_text = local_text
                transcript_meta.update(local_meta)
                transcript_meta["source"] = "local-asr"
                transcript_meta["available"] = True
                job.append_log("本地 `ASR` 完成。")
            else:
                job.append_log(local_meta.get("reason", "本地 `ASR` 不可用。"), level="warning")

        if not raw_transcript_text:
            job.append_log("本地 `ASR` 未产出文案，尝试云端转录兜底。")
            cloud_text, cloud_meta = transcribe_with_openai(audio_path)
            transcript_meta["attempts"].append({"source": "cloud-transcription", **cloud_meta, "success": bool(cloud_text)})
            if cloud_text:
                raw_transcript_text = cloud_text
                transcript_meta.update(cloud_meta)
                transcript_meta["source"] = "cloud-transcription"
                transcript_meta["available"] = True
                job.append_log("云端转录完成。")
            else:
                job.append_log(cloud_meta.get("reason", "云端转录不可用。"), level="warning")

        if not raw_transcript_text.strip():
            transcript_meta["source"] = "failed"
            transcript_meta["available"] = False
            metadata["transcript"] = transcript_meta
            raise StageError(current_stage, "没有拿到任何可用文案，任务在转录阶段停止。", transcript_meta)

        metadata["transcript"] = transcript_meta

        current_stage = "transcript_cleanup"
        job.set_stage(current_stage)
        cleaned_text = clean_transcript_text(raw_transcript_text)
        if not cleaned_text:
            raise StageError(current_stage, "转录文案为空，无法继续清洗。")
        job.append_log("文案清洗完成。")

        current_stage = "ai_distillation"
        job.set_stage(current_stage)
        distillation_body, distillation_meta = summarize_with_openai(cleaned_text, video_path.stem)
        if distillation_body:
            job.append_log("已使用云端模型完成内容整理。")
        else:
            fallback_reason = distillation_meta.get("reason")
            if fallback_reason:
                job.append_log(fallback_reason, level="warning")
            distillation_body, distillation_meta = heuristic_distillation(video_path.stem, cleaned_text)
            job.append_log("已回退到本地启发式整理。", level="warning")
        metadata["distillation"] = distillation_meta

        current_stage = "output_writing"
        job.set_stage(current_stage)
        raw_path = run_dir / "01-raw-transcript.md"
        clean_path = run_dir / "02-clean-transcript.md"
        distill_path = run_dir / "03-ai-distillation.md"

        raw_path.write_text(render_raw_transcript_markdown(video_path, raw_transcript_text, metadata["transcript"]), encoding="utf-8")
        clean_path.write_text(render_clean_transcript_markdown(video_path, cleaned_text, metadata["transcript"]), encoding="utf-8")
        distill_path.write_text(
            render_distillation_markdown(video_path, distillation_body, metadata["distillation"], metadata["transcript"]),
            encoding="utf-8",
        )
        metadata["artifacts"].update(
            {
                "raw_transcript": str(raw_path),
                "clean_transcript": str(clean_path),
                "distillation": str(distill_path),
                "job_log": str(run_dir / "job.log"),
            }
        )
        metadata["distillation_preview"] = distillation_body[:2000]
        metadata["status"] = "succeeded"
        metadata["duration_seconds"] = round(time.monotonic() - started, 2)
        meta_path = run_dir / "meta.json"
        write_json(meta_path, metadata)
        metadata["artifacts"]["meta"] = str(meta_path)
        write_json(meta_path, metadata)
        result_files = [
            {"label": "任务元数据", "path": str(meta_path)},
            {"label": "原始转录", "path": str(raw_path)},
            {"label": "清洗转录", "path": str(clean_path)},
            {"label": "蒸馏整理", "path": str(distill_path)},
            {"label": "执行日志", "path": str(run_dir / "job.log")},
        ]
        job.append_log("结果文件写入完成。")
        job.complete(metadata, result_files, distillation_body[:4000])
    except StageError as exc:
        metadata["status"] = "failed"
        metadata["duration_seconds"] = round(time.monotonic() - started, 2)
        metadata["failed_stage"] = exc.stage_key
        metadata["error"] = {"message": str(exc), "details": exc.details}
        if run_dir:
            if raw_transcript_text:
                raw_path = run_dir / "01-raw-transcript.md"
                raw_path.write_text(render_raw_transcript_markdown(Path(job.video_path), raw_transcript_text, metadata["transcript"]), encoding="utf-8")
                metadata["artifacts"]["raw_transcript"] = str(raw_path)
            if cleaned_text:
                clean_path = run_dir / "02-clean-transcript.md"
                clean_path.write_text(render_clean_transcript_markdown(Path(job.video_path), cleaned_text, metadata["transcript"]), encoding="utf-8")
                metadata["artifacts"]["clean_transcript"] = str(clean_path)
            meta_path = run_dir / "meta.json"
            metadata["artifacts"]["meta"] = str(meta_path)
            metadata["artifacts"]["job_log"] = str(run_dir / "job.log")
            write_json(meta_path, metadata)
        job.append_log(str(exc), level="error")
        job.fail(exc.stage_key, str(exc), metadata, exc.details)
    except Exception as exc:  # noqa: BLE001
        metadata["status"] = "failed"
        metadata["duration_seconds"] = round(time.monotonic() - started, 2)
        metadata["failed_stage"] = current_stage
        metadata["error"] = {"message": str(exc), "traceback": traceback.format_exc()}
        if run_dir:
            meta_path = run_dir / "meta.json"
            metadata["artifacts"]["meta"] = str(meta_path)
            metadata["artifacts"]["job_log"] = str(run_dir / "job.log")
            write_json(meta_path, metadata)
        job.append_log(f"未预期错误：{exc}", level="error")
        job.fail(current_stage, str(exc), metadata, {"traceback": traceback.format_exc()})


def can_import(module_name: str) -> bool:
    try:
        __import__(module_name)
    except Exception:  # noqa: BLE001
        return False
    return True

