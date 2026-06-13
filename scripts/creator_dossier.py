#!/usr/bin/env python3
"""Create or update a person-first creator dossier from a single source entry."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = REPO_ROOT / "raw"

TIME_PRECISIONS = ("exact", "date-only", "estimated", "unknown")
SOURCE_TYPES = ("video", "article", "book", "interview", "note", "other")


def now_iso() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S")


def today_iso() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d")


def safe_filename_part(value: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|\r\n\t]+", "_", value).strip(" ._")
    return cleaned or "未命名"


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "-", value).strip("-_")
    return cleaned or "source"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_stars(stars: int) -> int:
    if stars < 1 or stars > 5:
        raise ValueError("星级必须是 1-5 的整数")
    return stars


def doc_title_prefix(category: str) -> str:
    if category in ("两者都是", "AI 大神 + AI 创作者", "AI 大神"):
        return "AI 大神"
    return "AI 创作者"


def output_dir_name(category: str) -> str:
    if category in ("两者都是", "AI 大神 + AI 创作者", "AI 大神"):
        return "A_AI-Gurus(AI大神)"
    return "A_AI-Content-Creator(AI 创作者)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="接入单条来源并生成人物蒸馏档案")
    parser.add_argument("--creator-name", required=True, help="人物主名称")
    parser.add_argument("--category", required=True, help="分类：AI 大神 / AI 创作者 / 两者都是")
    parser.add_argument("--stars", required=True, type=int, help="星级（1-5）")
    parser.add_argument("--platform", required=True, help="来源平台名，例如 视频号 / 公众号 / 书籍")
    parser.add_argument("--source-type", choices=SOURCE_TYPES, required=True, help="来源类型")
    parser.add_argument("--seed-url", required=True, help="本次 seed 链接")
    parser.add_argument("--source-id", required=True, help="来源唯一标识，例如 视频ID / 文章ID / ISBN")
    parser.add_argument("--title", help="来源标题；不传则回退到描述或来源ID")
    parser.add_argument("--description", help="来源描述或摘要")
    parser.add_argument("--intro", help="人物简介；不传则优先取上游 JSON 的 intro/description")
    parser.add_argument("--avatar-url", help="头像 URL")
    parser.add_argument("--profile-url", help="人物主页 URL")
    parser.add_argument("--platform-id", help="平台人物 ID")
    parser.add_argument("--source-json", help="可选。上游来源 JSON 文件")
    parser.add_argument("--clipping-markdown", help="可选。原始 `Clippings` Markdown 路径")
    parser.add_argument("--cover-path", help="可选。原始封面文件路径")
    parser.add_argument("--local-video", help="可选。已下载到本地的视频文件路径")
    parser.add_argument("--published-at", help="精确发布时间，例如 2026-06-12T10:30:00+08:00")
    parser.add_argument("--published-date", help="只有日期时填写，例如 2026-06-12")
    parser.add_argument(
        "--published-precision",
        choices=TIME_PRECISIONS,
        default="unknown",
        help="发布时间精度：exact/date-only/estimated/unknown",
    )
    parser.add_argument(
        "--published-source",
        default="manual-input",
        help="发布时间来自哪里，例如 api.feed.publish_time / page-text / manual-input",
    )
    parser.add_argument(
        "--download-status",
        choices=("saved", "missing", "failed", "not-applicable"),
        default="missing",
        help="本地视频文件状态",
    )
    parser.add_argument("--download-note", default="", help="下载失败或缺失原因")
    parser.add_argument("--alias", action="append", default=[], help="可重复。补充别名")
    return parser.parse_args()


def resolve_source_json(args: argparse.Namespace) -> dict[str, Any]:
    if not args.source_json:
        return {}
    payload = load_json(Path(args.source_json).expanduser())
    return payload


def resolve_text(primary: str | None, *fallbacks: Any) -> str:
    for value in (primary, *fallbacks):
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def repo_relative(target: Path) -> str:
    try:
        return target.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return str(target.resolve())


def relative_link(from_dir: Path, target_repo_path: str) -> str:
    target = REPO_ROOT / target_repo_path
    return os.path.relpath(target, start=from_dir).replace(os.sep, "/")


def copy_artifact_if_present(source_path: str | None, target_dir: Path, target_name: str) -> dict[str, Any]:
    if not source_path:
        return {"path": "", "sha256": "", "size_bytes": 0}

    source = Path(source_path).expanduser()
    if not source.exists():
        return {"path": "", "sha256": "", "size_bytes": 0}

    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / target_name
    shutil.copy2(source, target)
    return {
        "path": repo_relative(target),
        "sha256": file_sha256(target),
        "size_bytes": target.stat().st_size,
    }


def ensure_creator_card(
    creator_card_path: Path,
    creator_name: str,
    category: str,
    stars: int,
    avatar_url: str,
    intro: str,
    platform: str,
    platform_id: str,
    profile_url: str,
) -> None:
    dossier_section = "### 资料索引\n- [[{stem}/来源索引]]\n- [[{stem}/人物蒸馏]]".format(stem=creator_card_path.stem)
    if creator_card_path.exists():
        text = creator_card_path.read_text(encoding="utf-8")
        if "### 资料索引" not in text:
            creator_card_path.write_text(text.rstrip() + "\n\n" + dossier_section + "\n", encoding="utf-8")
        return

    prefix = doc_title_prefix(category)
    tags = ["AI", "大神"] if prefix == "AI 大神" else ["AI", "创作者"]
    stars_str = "⭐️" * normalize_stars(stars)
    tags_yaml = "\n".join(f"  - {tag}" for tag in tags)
    category_value = "AI 大神" if prefix == "AI 大神" else "AI 创作者"
    body_intro = intro or "待补充。"
    markdown = f"""---
创建日期: {now_iso()}
tags:
{tags_yaml}
分类:
  - {category_value}
星级: {stars_str}
author_url: {avatar_url}
平台: {platform}
平台ID: {platform_id}
---

### 自我介绍
![{creator_name}|150]({avatar_url})
> {body_intro}

### 平台
- [**{platform}**]({profile_url or ''})

{dossier_section}
"""
    creator_card_path.parent.mkdir(parents=True, exist_ok=True)
    creator_card_path.write_text(markdown, encoding="utf-8")


def render_source_index(dossier: dict[str, Any], output_path: Path) -> None:
    creator = dossier["creator"]
    sources = dossier["sources"]
    category_tag = "大神" if creator["category"] == "AI 大神" else "创作者"
    lines: list[str] = [
        "---",
        f"创建日期: {dossier['created_at']}",
        "tags:",
        "  - AI",
        f"  - {category_tag}",
        "  - source-index",
        f"人物: {creator['name']}",
        "---",
        "",
        f"# {creator['name']}：来源索引",
        "",
        "## 人物主档",
        f"- 主名称：`{creator['name']}`",
        f"- 分类：`{creator['category']}`",
        f"- 平台身份线索：`{', '.join(creator['platform_labels']) or '待补充'}`",
        f"- 别名：`{', '.join(creator['aliases']) or '无'}`",
        "",
        "## 来源列表",
        "",
    ]

    for source in sources:
        publish_value = source.get("published_at") or source.get("published_date") or "未知"
        evidence_link = relative_link(output_path.parent, source["evidence_record"])
        engagement = source.get("engagement") or {}
        play_count = engagement.get("play_count") or "未返回"
        like_count = engagement.get("like_count") or "未返回"
        favorite_count = engagement.get("favorite_count") or "未返回"
        forward_count = engagement.get("forward_count") or "未返回"
        comment_count = engagement.get("comment_count") or "未返回"
        lines.extend(
            [
                f"### {source['title']}",
                f"- 来源平台：`{source['platform']}`",
                f"- 来源类型：`{source['source_type']}`",
                f"- 来源标识：`{source['source_id']}`",
                f"- seed 链接：[{source['seed_url']}]({source['seed_url']})",
                f"- 发布时间：`{publish_value}`",
                f"- 时间精度：`{source['published_precision']}`",
                f"- 时间来源：`{source['published_source']}`",
                f"- 互动数据：播放/阅读=`{play_count}`，点赞=`{like_count}`，收藏=`{favorite_count}`，转发=`{forward_count}`，评论=`{comment_count}`",
                f"- 本地视频：`{source['download_status']}`",
                f"- 证据文件：[{evidence_link}]({evidence_link})",
                "",
            ]
        )

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def render_distillation(dossier: dict[str, Any], output_path: Path) -> None:
    creator = dossier["creator"]
    sources = dossier["sources"]
    category_tag = "大神" if creator["category"] == "AI 大神" else "创作者"
    representative_lines: list[str] = []
    observation_lines: list[str] = []
    pending_lines: list[str] = []

    for source in sources:
        publish_value = source.get("published_at") or source.get("published_date") or "未知"
        representative_lines.append(
            f"- `[{source['platform']} | {source['source_type']}]` {source['title']} | 发布时间：`{publish_value}` | 时间精度：`{source['published_precision']}`"
        )
        description = source.get("description") or "待补充摘要。"
        observation_lines.append(
            f"- `From`：`{source['platform']}` / `ID={source['source_id']}` / 发布时间：`{publish_value}`\n  - 线索：{description}"
        )
        if source["download_status"] != "saved":
            pending_lines.append(
                f"- `视频证据不完整`：`{source['source_id']}` 当前本地视频状态为 `{source['download_status']}`，说明：{source.get('download_note') or '待补充'}"
            )
        if source["published_precision"] != "exact":
            pending_lines.append(
                f"- `发布时间待补强`：`{source['source_id']}` 当前时间精度为 `{source['published_precision']}`，来源：`{source['published_source']}`。"
            )

    if not pending_lines:
        pending_lines.append("- 暂无。")

    lines: list[str] = [
        "---",
        f"创建日期: {dossier['created_at']}",
        "tags:",
        "  - AI",
        f"  - {category_tag}",
        "  - distillation",
        f"人物: {creator['name']}",
        "---",
        "",
        f"# {creator['name']}：人物蒸馏",
        "",
        "## 人物简介",
        "",
        f"- 主名称：`{creator['name']}`",
        f"- 当前分类：`{creator['category']}`",
        f"- 平台身份线索：`{', '.join(creator['platform_labels']) or '待补充'}`",
        f"- 初始简介：{creator['intro'] or '待补充。'}",
        "",
        "## 核心主题",
        "",
        "- 待随着更多来源累积后归纳。目前先保留来源线索，不做过度判断。",
        "",
        "## 反复出现的观点",
        "",
        "- 当前来源不足以判定“反复出现”的稳定观点，后续补充 `公众号`、`书籍` 或更多视频后再升级。",
        "",
        "## 方法论",
        "",
        "- 当前来源不足以抽出稳定方法论，后续以多来源交叉验证后补充。",
        "",
        "## 初始观察",
        "",
        *observation_lines,
        "",
        "## 代表来源",
        "",
        *representative_lines,
        "",
        "## 待确认",
        "",
        *pending_lines,
        "",
    ]
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_source_entry(args: argparse.Namespace, source_payload: dict[str, Any], dossier_dir: Path) -> dict[str, Any]:
    source_id = args.source_id.strip()
    source_key = f"{slugify(args.platform)}:{source_id}"
    media_dir = dossier_dir / "媒体"
    evidence_dir = dossier_dir / "证据"

    video_artifact = copy_artifact_if_present(
        args.local_video,
        media_dir,
        f"{safe_filename_part(source_id)}{Path(args.local_video).suffix if args.local_video else '.mp4'}",
    )
    cover_artifact = copy_artifact_if_present(
        args.cover_path,
        media_dir,
        f"{safe_filename_part(source_id)}_cover{Path(args.cover_path).suffix if args.cover_path else '.jpg'}",
    )

    download_status = args.download_status
    if video_artifact["path"]:
        download_status = "saved"

    description = resolve_text(
        args.description,
        source_payload.get("description"),
        source_payload.get("intro"),
    )
    title = resolve_text(args.title, description, source_id)
    engagement = {
        "play_count": resolve_text(source_payload.get("play_count")),
        "like_count": resolve_text(source_payload.get("like_count")),
        "favorite_count": resolve_text(source_payload.get("favorite_count")),
        "forward_count": resolve_text(source_payload.get("forward_count")),
        "comment_count": resolve_text(source_payload.get("comment_count")),
    }

    evidence_record = evidence_dir / f"{slugify(args.platform)}-{safe_filename_part(source_id)}.json"
    entry = {
        "source_key": source_key,
        "platform": args.platform.strip(),
        "source_type": args.source_type,
        "source_id": source_id,
        "title": title,
        "description": description,
        "seed_url": args.seed_url.strip(),
        "profile_url": resolve_text(args.profile_url, source_payload.get("profile_url"), source_payload.get("space_url")),
        "platform_id": resolve_text(args.platform_id, source_payload.get("finder_id"), source_payload.get("mid")),
        "published_at": resolve_text(args.published_at),
        "published_date": resolve_text(args.published_date),
        "published_precision": args.published_precision,
        "published_source": args.published_source.strip(),
        "captured_at": now_iso(),
        "download_status": download_status,
        "download_note": args.download_note.strip(),
        "engagement": engagement,
        "evidence_record": repo_relative(evidence_record),
        "clipping_markdown": repo_relative(Path(args.clipping_markdown).expanduser()) if args.clipping_markdown else "",
        "raw_source_json": repo_relative(Path(args.source_json).expanduser()) if args.source_json else "",
        "original_cover_path": repo_relative(Path(args.cover_path).expanduser()) if args.cover_path else "",
        "original_local_video": repo_relative(Path(args.local_video).expanduser()) if args.local_video else "",
        "local_video_artifact": video_artifact,
        "cover_artifact": cover_artifact,
    }
    dump_json(evidence_record, entry)
    return entry


def merge_creator_info(
    existing: dict[str, Any] | None,
    args: argparse.Namespace,
    source_payload: dict[str, Any],
    creator_card_path: Path,
) -> dict[str, Any]:
    creator_name = args.creator_name.strip()
    intro = resolve_text(args.intro, source_payload.get("intro"), source_payload.get("description"))
    avatar_url = resolve_text(args.avatar_url, source_payload.get("avatar_url"))
    profile_url = resolve_text(args.profile_url, source_payload.get("profile_url"), source_payload.get("space_url"))
    platform_id = resolve_text(args.platform_id, source_payload.get("finder_id"), source_payload.get("mid"))
    platform_label = f"{args.platform}:{platform_id or args.source_id}"

    if existing is None:
        return {
            "name": creator_name,
            "category": args.category,
            "stars": normalize_stars(args.stars),
            "intro": intro,
            "avatar_url": avatar_url,
            "profile_url": profile_url,
            "aliases": sorted(set(args.alias)),
            "platform_labels": [platform_label],
            "seed_sources": [args.seed_url],
            "identity_review_notes": [],
            "creator_card": repo_relative(creator_card_path),
        }

    aliases = set(existing.get("aliases", []))
    aliases.update(filter(None, args.alias))
    if existing.get("name") != creator_name:
        aliases.add(creator_name)
        existing.setdefault("identity_review_notes", []).append(
            f"{now_iso()}：输入名称 `{creator_name}` 与现有人物主名称 `{existing.get('name')}` 不一致，已作为别名保留。"
        )

    platform_labels = set(existing.get("platform_labels", []))
    platform_labels.add(platform_label)
    seed_sources = set(existing.get("seed_sources", []))
    seed_sources.add(args.seed_url)

    existing.update(
        {
            "category": args.category,
            "stars": normalize_stars(args.stars),
            "intro": existing.get("intro") or intro,
            "avatar_url": existing.get("avatar_url") or avatar_url,
            "profile_url": existing.get("profile_url") or profile_url,
            "aliases": sorted(aliases),
            "platform_labels": sorted(platform_labels),
            "seed_sources": sorted(seed_sources),
            "creator_card": repo_relative(creator_card_path),
        }
    )
    return existing


def main() -> int:
    args = parse_args()
    normalize_stars(args.stars)
    source_payload = resolve_source_json(args)

    creator_name = args.creator_name.strip()
    prefix = doc_title_prefix(args.category)
    creator_card_path = RAW_ROOT / output_dir_name(args.category) / f"{prefix} - {safe_filename_part(creator_name)}.md"
    dossier_dir = creator_card_path.with_suffix("")
    dossier_json_path = dossier_dir / "档案.json"

    existing_dossier = load_json(dossier_json_path) if dossier_json_path.exists() else None
    creator_info = merge_creator_info(existing_dossier["creator"] if existing_dossier else None, args, source_payload, creator_card_path)

    ensure_creator_card(
        creator_card_path=creator_card_path,
        creator_name=creator_info["name"],
        category=args.category,
        stars=args.stars,
        avatar_url=creator_info["avatar_url"],
        intro=creator_info["intro"],
        platform=args.platform,
        platform_id=resolve_text(args.platform_id, source_payload.get("finder_id"), source_payload.get("mid"), args.source_id),
        profile_url=creator_info["profile_url"],
    )

    entry = build_source_entry(args, source_payload, dossier_dir)
    dossier = existing_dossier or {"created_at": now_iso(), "creator": creator_info, "sources": []}
    dossier["creator"] = creator_info
    dossier["updated_at"] = now_iso()

    updated_sources: list[dict[str, Any]] = []
    replaced = False
    for source in dossier["sources"]:
        if source["source_key"] == entry["source_key"]:
            updated_sources.append(entry)
            replaced = True
        else:
            updated_sources.append(source)
    if not replaced:
        updated_sources.append(entry)

    updated_sources.sort(key=lambda item: (item.get("published_at") or item.get("published_date") or "", item["source_key"]), reverse=True)
    dossier["sources"] = updated_sources

    dump_json(dossier_json_path, dossier)
    render_source_index(dossier, dossier_dir / "来源索引.md")
    render_distillation(dossier, dossier_dir / "人物蒸馏.md")

    print(json.dumps({"success": True, "creator_card": repo_relative(creator_card_path), "dossier_dir": repo_relative(dossier_dir)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
