from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .pipeline import JobState, can_import, now_iso, run_job


STATIC_DIR = Path(__file__).resolve().parent / "static"


class JobManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._job: JobState | None = None

    def current(self) -> JobState | None:
        with self._lock:
            return self._job

    def snapshot(self) -> dict[str, Any] | None:
        job = self.current()
        return job.snapshot() if job else None

    def start(self, video_path: str, output_dir: str) -> JobState:
        with self._lock:
            if self._job and self._job.status == "running":
                raise ValueError("当前已有任务运行中，请等待完成后再启动新任务。")
            job = JobState(
                job_id=f"job-{now_iso().replace(':', '').replace('+', '-').replace('T', '-')}",
                video_path=video_path,
                output_dir=output_dir,
            )
            self._job = job
            thread = threading.Thread(target=run_job, args=(job,), daemon=True, name=f"local-video-job-{job.job_id}")
            thread.start()
            return job


class LocalVideoWorkbenchHandler(BaseHTTPRequestHandler):
    job_manager: JobManager

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(HTTPStatus.NO_CONTENT)
        self._send_cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"/", "/index.html"}:
            self._serve_static("index.html", "text/html; charset=utf-8")
            return
        if self.path in {"/static/app.css", "/app.css"}:
            self._serve_static("app.css", "text/css; charset=utf-8")
            return
        if self.path in {"/static/app.js", "/app.js"}:
            self._serve_static("app.js", "application/javascript; charset=utf-8")
            return
        if self.path == "/api/job":
            self._send_json({"job": self.job_manager.snapshot()})
            return
        if self.path == "/api/capabilities":
            self._send_json(capability_payload())
            return
        self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/api/pick-video":
            self._handle_pick_file()
            return
        if self.path == "/api/pick-output-dir":
            self._handle_pick_folder()
            return
        if self.path == "/api/start-job":
            self._handle_start_job()
            return
        if self.path == "/api/open-output-dir":
            self._handle_open_output_dir()
            return
        self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        body = self.rfile.read(length)
        if not body:
            return {}
        return json.loads(body.decode("utf-8"))

    def _serve_static(self, name: str, content_type: str) -> None:
        target = STATIC_DIR / name
        if not target.exists():
            self._send_json({"error": "Missing static file"}, status=HTTPStatus.NOT_FOUND)
            return
        body = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self._send_cors_headers()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _handle_pick_file(self) -> None:
        try:
            path = run_native_picker("file")
        except RuntimeError as exc:
            self._send_json({"error": {"message": str(exc)}}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        if path is None:
            self._send_json({"cancelled": True})
            return
        self._send_json({"path": path})

    def _handle_pick_folder(self) -> None:
        try:
            path = run_native_picker("folder")
        except RuntimeError as exc:
            self._send_json({"error": {"message": str(exc)}}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        if path is None:
            self._send_json({"cancelled": True})
            return
        self._send_json({"path": path})

    def _handle_start_job(self) -> None:
        payload = self._read_json()
        video_path = str(payload.get("video_path", "")).strip()
        output_dir = str(payload.get("output_dir", "")).strip()
        if not video_path or not output_dir:
            self._send_json(
                {
                    "error": {
                        "message": "启动任务前必须同时提供视频文件和输出目录。",
                        "fields": {
                            "video_path": bool(video_path),
                            "output_dir": bool(output_dir),
                        },
                    }
                },
                status=HTTPStatus.BAD_REQUEST,
            )
            return
        try:
            job = self.job_manager.start(video_path=video_path, output_dir=output_dir)
        except ValueError as exc:
            self._send_json({"error": {"message": str(exc)}}, status=HTTPStatus.CONFLICT)
            return
        self._send_json({"job": job.snapshot()}, status=HTTPStatus.ACCEPTED)

    def _handle_open_output_dir(self) -> None:
        payload = self._read_json()
        target = str(payload.get("path", "")).strip()
        if not target:
            self._send_json({"error": {"message": "缺少要打开的路径。"}}, status=HTTPStatus.BAD_REQUEST)
            return
        path = Path(target).expanduser()
        if not path.exists():
            self._send_json({"error": {"message": f"路径不存在：`{path}`"}}, status=HTTPStatus.BAD_REQUEST)
            return
        result = subprocess.run(["open", str(path)], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            self._send_json(
                {"error": {"message": f"无法打开路径：`{path}`", "stderr": result.stderr.strip()}},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            return
        self._send_json({"opened": True, "path": str(path)})


def run_native_picker(selection_kind: str) -> str | None:
    result = subprocess.run(
        ["swift", "-e", picker_swift_script(selection_kind)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    stderr = result.stderr.strip()
    if "USER_CANCELLED" in stderr or result.returncode == 128:
        return None
    raise RuntimeError(stderr or "系统选择器执行失败。")


def picker_swift_script(selection_kind: str) -> str:
    if selection_kind == "file":
        prompt = "选择本地 MP4 文件"
        can_choose_files = "true"
        can_choose_directories = "false"
        allowed_types = 'panel.allowedFileTypes = ["mp4"]'
    else:
        prompt = "选择输出目录"
        can_choose_files = "false"
        can_choose_directories = "true"
        allowed_types = ""

    return f"""
import AppKit
import Foundation

let app = NSApplication.shared
app.setActivationPolicy(.regular)
app.activate(ignoringOtherApps: true)

let panel = NSOpenPanel()
panel.title = "{prompt}"
panel.message = "{prompt}"
panel.prompt = "选择"
panel.canChooseFiles = {can_choose_files}
panel.canChooseDirectories = {can_choose_directories}
panel.allowsMultipleSelection = false
panel.resolvesAliases = true
{allowed_types}

let response = panel.runModal()
if response == .OK, let url = panel.url {{
    print(url.path)
}} else {{
    FileHandle.standardError.write(Data("USER_CANCELLED\\n".utf8))
    Foundation.exit(128)
}}
"""


def capability_payload() -> dict[str, Any]:
    return {
        "ffmpeg_available": shutil_which("ffmpeg"),
        "ffprobe_available": shutil_which("ffprobe"),
        "local_asr_available": can_import("faster_whisper"),
        "openai_key_available": bool(os.getenv("OPENAI_API_KEY", "").strip()),
        "single_job_only": True,
        "accepted_input_suffixes": [".mp4"],
    }


def shutil_which(binary: str) -> str:
    return shutil.which(binary) or ""


def build_server(port: int) -> ThreadingHTTPServer:
    job_manager = JobManager()
    handler = type(
        "BoundLocalVideoWorkbenchHandler",
        (LocalVideoWorkbenchHandler,),
        {"job_manager": job_manager},
    )
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def main() -> int:
    parser = argparse.ArgumentParser(description="本地视频蒸馏工作台服务")
    parser.add_argument("--port", type=int, default=8765, help="监听端口，默认 `8765`")
    parser.add_argument("--no-open", action="store_true", help="启动后不要自动打开浏览器")
    args = parser.parse_args()

    server = build_server(args.port)
    url = f"http://127.0.0.1:{args.port}"
    print(f"片语蒸馏台已启动：{url}")
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n收到中断，准备退出。")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
