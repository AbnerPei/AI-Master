#!/usr/bin/env python3
"""Fetch a single WeChat Channels source and save clipping artifacts locally."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import requests


REPO_ROOT = Path(__file__).resolve().parents[1]
CLIPPINGS_DIR = REPO_ROOT / "Clippings" / "视频号"
API_URL = "https://channels.weixin.qq.com/finder-preview/api/feed/get_feed_info"
PROFILE_URL = "https://channels.weixin.qq.com/finder-preview/pages/sph?id={finder_id}"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
SHANGHAI_TZ = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S")


def safe_filename_part(value: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|\r\n\t]+", "_", value).strip(" ._")
    return cleaned or "未命名视频"


def normalize_count_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def extract_finder_id(target: str) -> str:
    value = target.strip()
    if re.fullmatch(r"[A-Za-z0-9_\-]{8,}", value):
        return value
    parsed = urlparse(value)
    host = parsed.netloc.lower()
    if host == "weixin.qq.com" and "/sph/" in parsed.path:
        short_id = parsed.path.rstrip("/").split("/")[-1]
        if re.fullmatch(r"[A-Za-z0-9_\-]{8,}", short_id):
            return short_id
    params = parse_qs(parsed.query)
    if "id" in params:
        return params["id"][0]
    match = re.search(r"sph[=/](\w+)", value)
    if match:
        return match.group(1)
    raise ValueError(f"无法从输入中解析 `finder_id`：{target}")


def fetch_raw_payload(finder_id: str) -> dict[str, Any]:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://channels.weixin.qq.com",
            "Referer": "https://channels.weixin.qq.com/",
        }
    )
    payload = {"baseReq": {"generalToken": ""}, "shortUri": finder_id}
    response = session.post(API_URL, json=payload, timeout=20)
    response.raise_for_status()
    data = response.json()
    if data.get("errCode") != 0:
        raise RuntimeError(data.get("errMsg") or f"`视频号` 接口返回 `errCode={data.get('errCode')}`")
    return data


def normalize_payload(finder_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    author = payload.get("data", {}).get("authorInfo", {}) or {}
    feed = payload.get("data", {}).get("feedInfo", {}) or {}
    description = str(feed.get("description") or "").strip()
    created_ts = feed.get("createtime")
    published_at = ""
    published_date = ""
    published_precision = "unknown"
    if isinstance(created_ts, int) and created_ts > 0:
        dt = datetime.fromtimestamp(created_ts, tz=SHANGHAI_TZ)
        published_at = dt.isoformat()
        published_date = dt.strftime("%Y-%m-%d")
        published_precision = "exact"

    title = description.splitlines()[0].strip() if description else finder_id
    profile_url = PROFILE_URL.format(finder_id=finder_id)
    like_count = normalize_count_text(feed.get("likeCountFmt"))
    favorite_count = normalize_count_text(feed.get("favCountFmt"))
    forward_count = normalize_count_text(feed.get("forwardCountFmt"))
    comment_count = normalize_count_text(feed.get("commentCountFmt"))
    play_count = normalize_count_text(
        feed.get("playCountFmt") or feed.get("readCountFmt") or feed.get("viewCountFmt")
    )
    return {
        "success": True,
        "platform": "视频号",
        "finder_id": finder_id,
        "name": str(author.get("nickname") or ""),
        "avatar_url": str(author.get("headImgUrl") or ""),
        "description": description,
        "title": title,
        "cover_url": str(feed.get("coverUrl") or ""),
        "profile_url": profile_url,
        "space_url": profile_url,
        "platform_id": finder_id,
        "published_at": published_at,
        "published_date": published_date,
        "published_precision": published_precision,
        "published_source": "feedInfo.createtime" if published_at else "api-missing",
        "raw_feed_createtime": created_ts or 0,
        "like_count": like_count,
        "favorite_count": favorite_count,
        "forward_count": forward_count,
        "comment_count": comment_count,
        "play_count": play_count,
        "engagement_available": any((like_count, favorite_count, forward_count, comment_count, play_count)),
    }


def download_cover_if_present(cover_url: str, output_path: Path) -> str:
    if not cover_url:
        return ""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(cover_url, timeout=20)
    response.raise_for_status()
    output_path.write_bytes(response.content)
    return str(output_path)


def write_markdown(meta: dict[str, Any], output_path: Path, cover_filename: str | None) -> None:
    published_value = meta.get("published_at") or meta.get("published_date") or "未知"
    cover_line = f"- **封面：** ![[{cover_filename}]]" if cover_filename else "- **封面：** 待补充"
    play_line = meta.get("play_count") or "未返回"
    like_line = meta.get("like_count") or "未返回"
    favorite_line = meta.get("favorite_count") or "未返回"
    forward_line = meta.get("forward_count") or "未返回"
    comment_line = meta.get("comment_count") or "未返回"
    markdown = f"""---
创建日期: {now_iso()}
来源: 视频号
作者: {meta['name']}
视频ID: {meta['finder_id']}
链接: {meta['profile_url']}
发布时间: {published_value}
发布时间精度: {meta['published_precision']}
---

## {meta['title']}

- **作者：** {meta['name']}
- **描述：** {meta['description']}
- **发布时间：** {published_value}
- **时间精度：** {meta['published_precision']}
- **播放 / 阅读：** {play_line}
- **点赞：** {like_line}
- **收藏：** {favorite_line}
- **转发：** {forward_line}
- **评论：** {comment_line}
{cover_line}

---

## 原始链接

[{meta['profile_url']}]({meta['profile_url']})
"""
    output_path.write_text(markdown, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="抓取单条 `视频号` 来源并落到 `Clippings/视频号/`")
    parser.add_argument("target", help="`视频号` 短链、页面链接或 `finder_id`")
    parser.add_argument("--download-cover", action="store_true", help="如果有封面 URL，则下载到本地")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    finder_id = extract_finder_id(args.target)
    raw_payload = fetch_raw_payload(finder_id)
    meta = normalize_payload(finder_id, raw_payload)

    CLIPPINGS_DIR.mkdir(parents=True, exist_ok=True)
    meta_path = CLIPPINGS_DIR / f"{finder_id}_meta.json"
    raw_path = CLIPPINGS_DIR / f"{finder_id}_raw.json"
    title_path = CLIPPINGS_DIR / f"{safe_filename_part(meta['title'])}.md"
    cover_path = CLIPPINGS_DIR / f"{finder_id}_cover.jpg"

    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raw_path.write_text(json.dumps(raw_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cover_filename = None
    if args.download_cover and meta["cover_url"]:
        download_cover_if_present(meta["cover_url"], cover_path)
        cover_filename = cover_path.name

    write_markdown(meta, title_path, cover_filename if cover_path.exists() else None)

    print(
        json.dumps(
            {
                "success": True,
                "finder_id": finder_id,
                "meta_path": str(meta_path.relative_to(REPO_ROOT)),
                "raw_path": str(raw_path.relative_to(REPO_ROOT)),
                "markdown_path": str(title_path.relative_to(REPO_ROOT)),
                "cover_path": str(cover_path.relative_to(REPO_ROOT)) if cover_path.exists() else "",
                "published_at": meta["published_at"],
                "published_precision": meta["published_precision"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
