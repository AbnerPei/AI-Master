#!/usr/bin/env python3
"""Compile a creator dossier into reusable local skill assets."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "raw" / "A_Tools(工具)" / "skills" / "generated"


def now_iso() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S")


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "-", value).strip("-_")
    return cleaned or "creator-skill"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def repo_rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def out_rel(output_dir: Path, target: Path) -> str:
    return os.path.relpath(target, start=output_dir).replace(os.sep, "/")


def render_skill_markdown(
    dossier: dict[str, Any],
    dossier_dir: Path,
    output_dir: Path,
    references_path: Path,
) -> str:
    creator = dossier["creator"]
    sources = dossier["sources"]
    creator_name = creator["name"]
    profile_link = creator.get("profile_url") or ""
    platform_labels = ", ".join(creator.get("platform_labels") or []) or "待补充"
    seed_line = "、".join(f"`{item}`" for item in creator.get("seed_sources") or []) or "待补充"
    trigger_terms = [creator_name, *creator.get("aliases", [])]
    trigger_terms.extend([label.split(":", 1)[0] for label in creator.get("platform_labels", [])])
    trigger_terms = sorted({term for term in trigger_terms if term})

    evidence_lines: list[str] = []
    for source in sources[:5]:
        publish_value = source.get("published_at") or source.get("published_date") or "未知"
        evidence_lines.append(
            f"- `[{source['platform']} | {source['source_type']}]` {source['title']} | 发布时间：`{publish_value}` | 时间精度：`{source['published_precision']}`"
        )
    if not evidence_lines:
        evidence_lines.append("- 暂无。")

    intro_lines = (creator.get("intro") or "").splitlines()
    skill_intro = intro_lines[0].strip() if intro_lines else f"围绕 `{creator_name}` 的人物理解与资料索引。"

    return f"""---
创建日期: {now_iso()}
tags:
  - AI
  - 工具
  - skills
  - creator-skill
人物: {creator_name}
---

## 这个 `skill` 是做什么的

这个 `skill` 用来在当前仓库里复用对 `{creator_name}` 的人物理解，而不是每次都重新从零整理资料。

它的核心作用有三件事：

- 遇到 `{creator_name}` 相关资料时，优先归并到同一个人物档案
- 基于已沉淀的来源索引和人物蒸馏，快速给出结构化理解
- 继续把新增的 `视频号`、`公众号`、`书籍` 等材料接到现有档案，而不是平行新建

## 什么时候用

当输入里出现下面这些触发线索时，优先想到这个 `skill`：

- {", ".join(f"`{item}`" for item in trigger_terms) if trigger_terms else "`待补充`"}
- 需要继续整理 `{creator_name}` 的新资料
- 需要基于 `{creator_name}` 的历史资料做总结、蒸馏或方法论归纳

## 能力边界

这个 `skill` 适合：

- 补充同一人物的新来源
- 读取已沉淀的人物档案、来源索引和证据记录
- 基于现有证据做保守总结，而不是脱离证据发挥

这个 `skill` 不适合：

- 把单条 `seed` 误判成创作者全量内容
- 把原始证据直接改写成确定结论而不保留回链
- 在没有新证据时伪造“反复出现的稳定观点”

## 当前人物理解

- 人物：`{creator_name}`
- 简介线索：{skill_intro}
- 平台身份线索：`{platform_labels}`
- 已知 `seed`：{seed_line}
- 主页链接：{f"[{profile_link}]({profile_link})" if profile_link else "待补充"}

## 当前代表证据

{chr(10).join(evidence_lines)}

## 使用原则

1. 先查档案，再决定是否新增来源。
2. 对视频类来源，优先保留本地视频副本；如果没有，也要显式记录缺失原因。
3. 对时间信息，必须保留 `published_at`、`published_precision` 和时间来源，不能把模糊时间伪装成精确时间。
4. 做结论时，要优先回链到来源索引或证据 `JSON`，不要只保留一句脱离上下文的摘要。

## 参考资料

- 人物档案目录：[{dossier_dir.name}]({out_rel(output_dir, dossier_dir)})
- 参考资料索引：[{references_path.name}]({references_path.name})
"""


def render_references_markdown(
    dossier: dict[str, Any],
    dossier_dir: Path,
    output_dir: Path,
) -> str:
    creator = dossier["creator"]
    creator_card = REPO_ROOT / creator["creator_card"]
    source_index = dossier_dir / "来源索引.md"
    distillation = dossier_dir / "人物蒸馏.md"
    dossier_json = dossier_dir / "档案.json"

    lines = [
        "---",
        f"创建日期: {now_iso()}",
        "tags:",
        "  - AI",
        "  - 工具",
        "  - skills",
        "  - references",
        f"人物: {creator['name']}",
        "---",
        "",
        f"# {creator['name']}：`skill` 参考资料索引",
        "",
        "## 主档回链",
        f"- 人物卡片：[/{repo_rel(creator_card)}]({out_rel(output_dir, creator_card)})",
        f"- 档案 `JSON`：[/{repo_rel(dossier_json)}]({out_rel(output_dir, dossier_json)})",
        f"- 来源索引：[/{repo_rel(source_index)}]({out_rel(output_dir, source_index)})",
        f"- 人物蒸馏：[/{repo_rel(distillation)}]({out_rel(output_dir, distillation)})",
        "",
        "## 证据列表",
        "",
    ]

    for source in dossier["sources"]:
        evidence = REPO_ROOT / source["evidence_record"]
        publish_value = source.get("published_at") or source.get("published_date") or "未知"
        lines.extend(
            [
                f"### {source['title']}",
                f"- 证据 `JSON`：[/{repo_rel(evidence)}]({out_rel(output_dir, evidence)})",
                f"- 来源平台：`{source['platform']}`",
                f"- 发布时间：`{publish_value}`",
                f"- 时间精度：`{source['published_precision']}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从人物档案编译仓库内可复用的 `skill` 资产")
    parser.add_argument(
        "--dossier-dir",
        required=True,
        help="人物档案目录，例如 `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 姜胡说`",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dossier_dir = Path(args.dossier_dir).expanduser().resolve()
    dossier_json = dossier_dir / "档案.json"
    if not dossier_json.exists():
        raise FileNotFoundError(f"未找到人物档案：{dossier_json}")

    dossier = load_json(dossier_json)
    creator_name = dossier["creator"]["name"]
    output_dir = SKILL_ROOT / slugify(creator_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    references_path = output_dir / "参考资料索引.md"
    skill_path = output_dir / "SKILL.md"
    manifest_path = output_dir / "skill-manifest.json"

    references_path.write_text(
        render_references_markdown(dossier, dossier_dir, output_dir),
        encoding="utf-8",
    )
    skill_path.write_text(
        render_skill_markdown(dossier, dossier_dir, output_dir, references_path),
        encoding="utf-8",
    )

    manifest = {
        "created_at": now_iso(),
        "creator_name": creator_name,
        "source_dossier_dir": repo_rel(dossier_dir),
        "skill_markdown": repo_rel(skill_path),
        "references_markdown": repo_rel(references_path),
        "source_count": len(dossier["sources"]),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "success": True,
                "creator_name": creator_name,
                "skill_dir": repo_rel(output_dir),
                "skill_path": repo_rel(skill_path),
                "references_path": repo_rel(references_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
