#!/usr/bin/env python3
"""Enumerate a creator-scoped WeChat Channels catalog from a single seed video."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

from fetch_wechat_channels_source import (
    CLIPPINGS_DIR,
    DEFAULT_USER_AGENT,
    extract_finder_id,
    fetch_raw_payload,
    normalize_payload,
    safe_filename_part,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
QUEUE_STATES = ("pending", "downloaded", "metadata-only", "failed", "review-required")
LOCAL_API_BASE = "http://127.0.0.1:2022"


def now_iso() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S")


def fetch_public_seed_page(seed_url: str) -> tuple[str, dict[str, Any]]:
    response = requests.get(
        seed_url,
        headers={"User-Agent": DEFAULT_USER_AGENT},
        timeout=20,
    )
    response.raise_for_status()
    html = response.text
    inspection = {
        "status_code": response.status_code,
        "content_length": len(html),
        "has_app_root": '<div id="app"></div>' in html,
        "has_feed_bundle": "feed." in html and "finder-preview" in html,
        "has_embedded_creator_list": bool(
            re.search(r"author(List|Feed|Profile)|creator(List|Profile)|feedList", html, flags=re.IGNORECASE)
        ),
    }
    return html, inspection


def fetch_local_api_status() -> dict[str, Any] | None:
    try:
        response = requests.get(f"{LOCAL_API_BASE}/api/status", timeout=3)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return None
    if payload.get("code") != 0:
        return None
    return payload.get("data") or {}


def fetch_local_api_payload(path: str, params: dict[str, str]) -> dict[str, Any]:
    response = requests.get(
        f"{LOCAL_API_BASE}{path}",
        params=params,
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("code") != 0:
        raise RuntimeError(payload.get("msg") or f"本地 `API` 调用失败：{path}")
    return payload.get("data") or {}


def search_creator_contact(creator_name: str) -> dict[str, Any] | None:
    if not creator_name.strip():
        return None
    data = fetch_local_api_payload("/api/channels/contact/search", {"keyword": creator_name.strip()})
    candidates = data.get("infoList") or []
    if not candidates:
        return None

    def score(candidate: dict[str, Any]) -> tuple[int, int]:
        contact = candidate.get("contact") or {}
        nickname = str(contact.get("nickname") or "").strip()
        signature = str(contact.get("signature") or "").strip()
        exact = int(nickname == creator_name.strip())
        contains = int(creator_name.strip() in nickname or nickname in creator_name.strip())
        signature_hit = int(bool(signature) and creator_name.strip() in signature)
        return (exact, contains + signature_hit)

    return max(candidates, key=score)


def build_public_strategy_trace(page_probe: dict[str, Any], local_status: dict[str, Any] | None) -> list[dict[str, Any]]:
    local_connected = bool(local_status)
    local_available = bool(local_status and (local_status.get("channels") or {}).get("available"))
    trace = [
        {
            "name": "feed_info_api",
            "type": "public-response",
            "status": "success",
            "priority": 1,
            "notes": "通过单条 `shortUri` 接口拿到 seed 视频元数据和可见作者名称。",
        },
        {
            "name": "public_seed_page",
            "type": "public-page",
            "status": "success" if page_probe["status_code"] == 200 else "failed",
            "priority": 2,
            "notes": (
                "当前公开 seed 页面是前端壳页，未直接内嵌创作者全量内容列表。"
                if page_probe["has_app_root"] and page_probe["has_feed_bundle"]
                else "当前公开 seed 页面结构与预期不一致，需要复核。"
            ),
        },
        {
            "name": "public_creator_catalog",
            "type": "public-catalog",
            "status": "unavailable",
            "priority": 3,
            "notes": "当前公开 seed 页面和单条 feed 接口都没有暴露稳定的创作者全量列表入口或创作者主键。",
        },
        {
            "name": "wx_channels_download_local_api",
            "type": "desktop-bridge",
            "status": (
                "success"
                if local_available
                else "waiting"
                if local_connected
                else "offline"
            ),
            "priority": 4,
            "notes": (
                "本地 `wx_channels_download` 服务已连接到 `WeChat` 前端，可继续用主页分页接口拿全量列表。"
                if local_available
                else "本地 `wx_channels_download` 服务已启动，但 `channels.available=false`；通常说明 `WeChat` 尚未打开视频号页、前端注入未建立，或桌面 `WeChat` 处于锁定状态。"
                if local_connected
                else "本地 `wx_channels_download` 服务未启动，无法使用主页分页接口。"
            ),
        },
        {
            "name": "mac_wechat_automation",
            "type": "desktop-fallback",
            "status": "required",
            "priority": 5,
            "notes": "若要追求创作者全量遍历，需要在 `Mac WeChat` 中做主页级或列表级自动化，而不是人工逐条点开。",
        },
    ]
    return trace


def build_local_strategy_trace(page_probe: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "name": "feed_info_api",
            "type": "public-response",
            "status": "success",
            "priority": 1,
            "notes": "通过单条 `shortUri` 接口拿到 seed 视频元数据和可见作者名称。",
        },
        {
            "name": "wx_channels_download_local_api",
            "type": "desktop-bridge",
            "status": "success",
            "priority": 2,
            "notes": "通过 `wx_channels_download` 本地 `API` 搜索创作者并按主页分页接口遍历内容列表。",
        },
        {
            "name": "public_seed_page",
            "type": "public-page",
            "status": "success" if page_probe["status_code"] == 200 else "failed",
            "priority": 3,
            "notes": "公开 seed 页面继续作为发布时间、页面结构和后续人工复核的辅助证据。",
        },
    ]


def build_catalog_entry(meta: dict[str, Any], seed_url: str) -> dict[str, Any]:
    queue_status = "metadata-only"
    if queue_status not in QUEUE_STATES:
        raise ValueError(f"不支持的 `queue_status`：{queue_status}")

    published_value = meta.get("published_at") or meta.get("published_date") or ""
    return {
        "catalog_key": f"视频号:{meta['finder_id']}",
        "platform": "视频号",
        "source_id": meta["finder_id"],
        "title": meta["title"],
        "description": meta.get("description") or "",
        "source_url": meta["profile_url"],
        "seed_url": seed_url,
        "cover_url": meta.get("cover_url") or "",
        "published_at": meta.get("published_at") or "",
        "published_date": meta.get("published_date") or "",
        "published_value": published_value,
        "published_precision": meta.get("published_precision") or "unknown",
        "published_source": meta.get("published_source") or "unknown",
        "play_count": meta.get("play_count") or "",
        "like_count": meta.get("like_count") or "",
        "favorite_count": meta.get("favorite_count") or "",
        "forward_count": meta.get("forward_count") or "",
        "comment_count": meta.get("comment_count") or "",
        "discovery_strategy": "feed_info_api",
        "discovery_source": "shortUri",
        "queue_status": queue_status,
        "download_status": "missing",
        "download_note": "当前仅确认到 seed 视频元数据；本地视频与创作者全量列表需后续补采。",
        "review_required": True,
    }


def build_local_catalog_entry(
    obj: dict[str, Any],
    creator_username: str,
    seed_url: str,
) -> dict[str, Any]:
    description = str(((obj.get("objectDesc") or {}).get("description")) or "").strip()
    title = description.splitlines()[0].strip() if description else str(obj.get("id") or obj.get("objectNonceId") or "未命名视频")
    media_items = ((obj.get("objectDesc") or {}).get("media")) or []
    cover_url = ""
    if media_items:
        cover_url = str((media_items[0] or {}).get("coverUrl") or "")
    created_ts = obj.get("createtime")
    published_at = ""
    published_date = ""
    if isinstance(created_ts, int) and created_ts > 0:
        dt = datetime.fromtimestamp(created_ts).astimezone()
        published_at = dt.strftime("%Y-%m-%dT%H:%M:%S%z")
        published_date = dt.strftime("%Y-%m-%d")

    return {
        "catalog_key": f"视频号:{obj.get('id') or obj.get('objectNonceId')}",
        "platform": "视频号",
        "source_id": str(obj.get("id") or ""),
        "nonce_id": str(obj.get("objectNonceId") or ""),
        "creator_username": creator_username,
        "title": title,
        "description": description,
        "source_url": str(obj.get("source_url") or ""),
        "seed_url": seed_url,
        "cover_url": cover_url,
        "published_at": published_at,
        "published_date": published_date,
        "published_value": published_at or published_date,
        "published_precision": "exact" if published_at else "unknown",
        "published_source": "wx_channels_download.contact.feed.list.createtime",
        "discovery_strategy": "wx_channels_download_local_api",
        "discovery_source": "contact.feed.list",
        "queue_status": "metadata-only",
        "download_status": "missing",
        "download_note": "已通过创作者主页分页拿到条目元数据，尚未执行本地视频下载。",
        "review_required": False,
    }


def build_public_catalog(
    meta: dict[str, Any],
    seed_url: str,
    page_probe: dict[str, Any],
    local_status: dict[str, Any] | None,
) -> dict[str, Any]:
    entry = build_catalog_entry(meta, seed_url)
    queue_counter = Counter([entry["queue_status"]])
    published_counter = Counter([entry["published_precision"]])
    local_connected = bool(local_status)

    return {
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "platform": "视频号",
        "seed": {
            "seed_url": seed_url,
            "finder_id": meta["finder_id"],
            "seed_title": meta["title"],
        },
        "creator": {
            "name": meta.get("name") or "",
            "avatar_url": meta.get("avatar_url") or "",
            "profile_url": meta.get("profile_url") or "",
            "platform_creator_id": "",
            "identity_status": "provisional",
            "identity_note": "当前公开单条 feed 接口未返回稳定的创作者主键，先以可见名称建立暂存身份。",
        },
        "enumeration": {
            "catalog_status": "partial",
            "expected_total_known": False,
            "discovered_count": 1,
            "queue_state_counts": dict(queue_counter),
            "published_precision_counts": dict(published_counter),
            "downloaded_video_count": 0,
            "page_probe": page_probe,
            "local_api_status": local_status or {},
            "strategy_trace": build_public_strategy_trace(page_probe, local_status),
            "failure_reasons": [
                "当前公开 seed 页面仅暴露前端壳页，未直接给出创作者全量内容列表。",
                "当前公开单条 feed 接口能确认 seed 视频，但未给出稳定的创作者全量枚举主键。",
                *(
                    [
                        "本地 `wx_channels_download` 服务虽然已启动，但尚未和 `WeChat` 视频号前端建立连接。"
                    ]
                    if local_connected and not (local_status.get("channels") or {}).get("available")
                    else []
                ),
            ],
            "coverage_note": "本次结果只能确认 seed 视频已存在，不代表已拿到该创作者全部视频。",
            "next_steps": [
                "如果本地 `API` 已启动但 `channels.available=false`，先解锁 `Mac WeChat`，再打开任意视频号页建立前端连接。",
                "继续尝试从后续网页 bundle 或响应里定位创作者主页级接口。",
                "如果公开路径仍不足，则转入 `Mac WeChat` 主页级自动化遍历。",
                "对已发现条目逐步补齐本地视频、副标题、转写稿和发布时间复核。",
            ],
        },
        "entries": [entry],
    }


def build_local_catalog(
    meta: dict[str, Any],
    seed_url: str,
    page_probe: dict[str, Any],
    local_status: dict[str, Any],
) -> dict[str, Any] | None:
    creator_name = str(meta.get("name") or "").strip()
    candidate = search_creator_contact(creator_name)
    if not candidate:
        return None

    contact = candidate.get("contact") or {}
    username = str(contact.get("username") or "").strip()
    if not username:
        return None

    entries: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    next_marker = ""
    expected_total = 0
    page_count = 0
    continue_flag = 0
    last_buffer = ""
    creator_contact = contact

    while True:
        page_count += 1
        payload = fetch_local_api_payload(
            "/api/channels/contact/feed/list",
            {"username": username, "next_marker": next_marker},
        )
        creator_contact = payload.get("contact") or creator_contact
        expected_total = max(expected_total, int(payload.get("feedsCount") or 0))
        continue_flag = int(payload.get("continueFlag") or 0)
        last_buffer = str(payload.get("lastBuffer") or "")

        for obj in payload.get("object") or []:
            dedupe_key = str(obj.get("id") or obj.get("objectNonceId") or "")
            if not dedupe_key or dedupe_key in seen_ids:
                continue
            seen_ids.add(dedupe_key)
            entries.append(build_local_catalog_entry(obj, username, seed_url))

        if continue_flag == 0 or not last_buffer or last_buffer == next_marker:
            break
        next_marker = last_buffer
        if page_count >= 50:
            break

    if not entries:
        return None

    queue_counter = Counter(entry["queue_status"] for entry in entries)
    published_counter = Counter(entry["published_precision"] for entry in entries)
    is_complete = continue_flag == 0 and (expected_total == 0 or len(entries) >= expected_total)
    coverage_note = (
        f"已通过本地 `API` 分页拿到 `{len(entries)}``/``{expected_total}` 条主页内容。"
        if expected_total
        else f"已通过本地 `API` 分页拿到 `{len(entries)}` 条主页内容，平台未明确返回总数。"
    )

    return {
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "platform": "视频号",
        "seed": {
            "seed_url": seed_url,
            "finder_id": meta["finder_id"],
            "seed_title": meta["title"],
        },
        "creator": {
            "name": str(creator_contact.get("nickname") or creator_name),
            "avatar_url": str(creator_contact.get("headUrl") or meta.get("avatar_url") or ""),
            "profile_url": str(meta.get("profile_url") or ""),
            "platform_creator_id": username,
            "identity_status": "confirmed",
            "identity_note": "已通过 `wx_channels_download` 的创作者搜索和主页分页接口确认创作者身份。",
            "signature": str(creator_contact.get("signature") or ""),
        },
        "enumeration": {
            "catalog_status": "complete" if is_complete else "partial",
            "expected_total_known": bool(expected_total),
            "expected_total": expected_total,
            "discovered_count": len(entries),
            "queue_state_counts": dict(queue_counter),
            "published_precision_counts": dict(published_counter),
            "downloaded_video_count": 0,
            "page_probe": page_probe,
            "local_api_status": local_status,
            "strategy_trace": build_local_strategy_trace(page_probe),
            "failure_reasons": [] if is_complete else ["创作者主页分页在本次会话中未确认收敛到全量，需要复核 `lastBuffer` 或重新触发前端列表加载。"],
            "coverage_note": coverage_note,
            "next_steps": [
                "继续调用下载任务接口，把枚举结果转成批量下载队列。",
                "把每条视频的本地副本、转写稿和发布时间复核结果补回人物档案。",
            ],
        },
        "entries": entries,
    }


def write_markdown(catalog: dict[str, Any], output_path: Path) -> None:
    creator = catalog["creator"]
    enumeration = catalog["enumeration"]
    entries = catalog["entries"]
    entry = entries[0]
    lines = [
        "---",
        f"创建日期: {catalog['created_at']}",
        "来源: 视频号",
        f"人物: {creator['name'] or '待确认'}",
        f"seed: {catalog['seed']['seed_url']}",
        f"状态: {enumeration['catalog_status']}",
        "---",
        "",
        f"# {creator['name'] or '待确认'}：创作者内容枚举",
        "",
        "## 本次结论",
        "",
        f"- 枚举状态：`{enumeration['catalog_status']}`",
        f"- 已发现条目数：`{enumeration['discovered_count']}`",
        f"- 是否已知全量总数：`{enumeration['expected_total_known']}`",
        f"- 覆盖说明：{enumeration['coverage_note']}",
        "",
        "## 创作者身份",
        "",
        f"- 名称：`{creator['name'] or '待确认'}`",
        f"- 主页链接：[{creator['profile_url']}]({creator['profile_url']})" if creator["profile_url"] else "- 主页链接：待确认",
        f"- 身份状态：`{creator['identity_status']}`",
        f"- 身份说明：{creator['identity_note']}",
        "",
        "## 条目概览",
        "",
        f"- 首条标题：`{entry['title']}`",
        f"- 首条来源链接：[{entry['source_url']}]({entry['source_url']})" if entry["source_url"] else "- 首条来源链接：待补充",
        f"- 首条发布时间：`{entry['published_value'] or '未知'}`",
        f"- 首条时间精度：`{entry['published_precision']}`",
        f"- 队列状态分布：`{json.dumps(enumeration['queue_state_counts'], ensure_ascii=False)}`",
        "",
        "## 策略轨迹",
        "",
    ]

    for strategy in enumeration["strategy_trace"]:
        lines.extend(
            [
                f"### {strategy['name']}",
                f"- 类型：`{strategy['type']}`",
                f"- 优先级：`{strategy['priority']}`",
                f"- 状态：`{strategy['status']}`",
                f"- 说明：{strategy['notes']}",
                "",
            ]
        )

    lines.extend(
        [
            "## 前十条条目",
            "",
        ]
    )
    for index, current in enumerate(entries[:10], start=1):
        source_line = (
            f"- 链接：[{current['source_url']}]({current['source_url']})"
            if current["source_url"]
            else "- 链接：待补充"
        )
        lines.extend(
            [
                f"### {index}. {current['title']}",
                f"- 发布时间：`{current['published_value'] or '未知'}`",
                f"- 时间精度：`{current['published_precision']}`",
                source_line,
                f"- 下载状态：`{current['download_status']}`",
                "",
            ]
        )

    lines.extend(
        [
            "## 失败原因",
            "",
            *([f"- {reason}" for reason in enumeration["failure_reasons"]] or ["- 无"]),
            "",
            "## 后续动作",
            "",
            *[f"- {step}" for step in enumeration["next_steps"]],
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从单条 `视频号` seed 枚举创作者内容清单")
    parser.add_argument("target", help="`视频号` 短链、页面链接或 `finder_id`")
    parser.add_argument(
        "--seed-url",
        help="显式提供原始 seed URL；默认回退到输入 target 或规范化后的页面链接",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    finder_id = extract_finder_id(args.target)
    raw_payload = fetch_raw_payload(finder_id)
    meta = normalize_payload(finder_id, raw_payload)
    seed_url = (args.seed_url or args.target).strip()

    html, page_probe = fetch_public_seed_page(seed_url)
    _ = html
    local_status = fetch_local_api_status()
    catalog = None
    if local_status and (local_status.get("channels") or {}).get("available"):
        try:
            catalog = build_local_catalog(meta, seed_url, page_probe, local_status)
        except Exception as exc:
            page_probe["local_api_error"] = str(exc)

    if catalog is None:
        catalog = build_public_catalog(meta, seed_url, page_probe, local_status)

    CLIPPINGS_DIR.mkdir(parents=True, exist_ok=True)
    meta_path = CLIPPINGS_DIR / f"{finder_id}_meta.json"
    raw_path = CLIPPINGS_DIR / f"{finder_id}_raw.json"
    catalog_json_path = CLIPPINGS_DIR / f"{finder_id}_catalog.json"
    catalog_md_path = CLIPPINGS_DIR / f"{safe_filename_part(meta['name'] or finder_id)}_内容枚举.md"

    if not meta_path.exists():
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not raw_path.exists():
        raw_path.write_text(json.dumps(raw_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    catalog_json_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(catalog, catalog_md_path)

    print(
        json.dumps(
            {
                "success": True,
                "finder_id": finder_id,
                "creator_name": meta.get("name") or "",
                "catalog_status": catalog["enumeration"]["catalog_status"],
                "discovered_count": catalog["enumeration"]["discovered_count"],
                "catalog_json_path": str(catalog_json_path.relative_to(REPO_ROOT)),
                "catalog_markdown_path": str(catalog_md_path.relative_to(REPO_ROOT)),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
