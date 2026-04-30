---
title: LLM Wiki
created: 2026-04-30
updated: 2026-04-30
type: concept
tags: [ai, llm, rag, workflow, tooling, automation]
sources: [../../raw/A_AI-Agent-Tech-Stack/L_LLM-Wiki/LLM Wiki 详解.md, ../../raw/A_Articles(文章)/I_Important-Articles(重量级文章)/LLM Knowledge Bases.md]
confidence: medium
---

# LLM Wiki

## 定义

LLM Wiki 是一种让 LLM Agent 持续维护 Markdown 知识库的方法：资料进入 raw 层，Agent 将其中的实体、概念、观点、流程和冲突增量整理进 wiki 层，并通过 `index.md`、`log.md`、frontmatter、Obsidian 双链 和 manifest 保持可追溯、可浏览、可 lint。

与一次性 [[LLM Knowledge Bases]] 摘要或普通 [[AI 资源索引]] 不同，LLM Wiki 的目标是形成会复利的知识资产：每次导入、查询、复盘和输出都反哺已有页面，而不是让同样的综合工作在聊天窗口里反复发生。

## 核心差异

| 维度 | RAG / 文件问答 | LLM Wiki |
|---|---|---|
| 知识形态 | 原始文档 + 检索索引 | 显性的 Markdown 页面网络 |
| 综合时机 | 每次提问时临时拼装 | 导入和更新时持续编译 |
| 可维护性 | 依赖应用和索引 | 可读、可 diff、可 Git 管理 |
| 复利能力 | 弱 | 强 |
| 适合场景 | 快速问答、海量检索 | 长期学习、研究、项目经验沉淀 |

## 对 AI-Master 的意义

AI-Master 本身就采用 `SCHEMA.md`、`raw/`、`wiki/`、`source-manifest.md` 的分层结构，因此 LLM Wiki 应被视为整个知识库的底层维护方法论，而不是单篇文章主题。

后续整理 AI 资料时，应优先遵守：

- 外部来源、用户原始资料、网页/PDF/OCR 派生内容进入 `raw/`；
- 综合判断、学习笔记、概念解释、操作流程进入 `wiki/`；
- 新页面必须更新 [[AI 资源索引]] 或 `wiki/index.md` 中相应导航；
- 重要查询结果如果有复用价值，应沉淀为 query、comparison、concept 或 playbook；
- 大改动后执行链接、manifest、frontmatter、敏感字段和 Git diff 验证。

## 关键工作流

1. 定向：读取 `SCHEMA.md`、`wiki/index.md`、最近 `wiki/log.md`。
2. 导入：保存 raw、记录来源、计算哈希、更新 `raw/source-manifest.md`。
3. 编译：把资料拆解到实体页、概念页、比较页、操作手册、学习笔记等。
4. 连接：补 Obsidian 双链、来源路径、tag、confidence。
5. 导航：更新 `wiki/index.md`、元信息页和日志。
6. 验证：检查断链、孤儿页、manifest 计数、敏感字段、`git diff --check`。

## 配图

![LLM Wiki 工作流](../../raw/A_Assets%28素材%29/L_LLM-Wiki/llm-wiki-workflow.svg)

## 相关页面

- [[LLM Knowledge Bases]]：Karpathy 关于 LLM 知识库模式的长帖整理。
- [[AI 资源索引]]：AI-Master 当前 raw 与 wiki 资料导航。
- [[Hermes Agent]]：可作为维护 LLM Wiki 的 CLI Agent / 自动化工具。

## Sources

- [LLM Wiki 详解](../../raw/A_AI-Agent-Tech-Stack/L_LLM-Wiki/LLM%20Wiki%20详解.md)
- [LLM Knowledge Bases](../../raw/A_Articles%28文章%29/I_Important-Articles%28重量级文章%29/LLM%20Knowledge%20Bases.md)
