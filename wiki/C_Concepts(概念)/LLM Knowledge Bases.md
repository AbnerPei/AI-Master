---
title: LLM Knowledge Bases
created: 2026-04-30
updated: 2026-04-30
type: concept
tags: [ai, llm, rag, tooling, workflow, automation]
sources: [../../raw/A_Articles(文章)/I_Important-Articles(重量级文章)/LLM Knowledge Bases.md]
confidence: medium
---

# LLM Knowledge Bases

## 核心观点

[[Andrej Karpathy]] 在 2026-04-02 的长帖中把 LLM 知识库描述为一个由 LLM 维护的 Markdown 知识系统：原始资料进入 `raw/`，LLM 增量“编译”出带摘要、反向链接、分类、概念文章和交叉链接的 wiki，再由 Obsidian 作为阅读、浏览和可视化前端。

这个模式与传统 [[AI 资源索引]] 式资料导航不同：重点不是每次提问都从零检索，而是让探索、问答、输出和 lint 结果持续回流到知识库，使知识沉淀可以复利增长。

## 工作流分解

| 环节 | Karpathy 描述 | 对 AI-Master 的启发 |
|---|---|---|
| Data ingest | 将文章、论文、仓库、数据集、图片等索引到 `raw/`，再用 LLM 编译 wiki | 继续保持 `raw/` 与 `wiki/` 分层；source manifest 是 raw 层可追溯性的关键 |
| IDE | Obsidian 作为前端，查看 raw、compiled wiki 与派生可视化 | AI-Master 应保持 Markdown、wikilink、相对路径对 Obsidian 友好 |
| Q&A | wiki 达到一定规模后，LLM 可以围绕 wiki 回答复杂问题 | 重要回答应归档到 `wiki/Q_Queries(查询)/` 或概念页，避免重复推导 |
| Output | 输出 Markdown、Marp slides、matplotlib images，再回看或归档 | 未来可为文章、课程、实验建立可视化和演示层 |
| Linting | 用 LLM 做健康检查，发现不一致、缺失数据和新文章候选 | AI-Master 后续应定期检查断链、缺失来源、低置信度页面和过大页面 |
| Extra tools | 为 wiki 编写搜索引擎和 CLI 工具，供人和 LLM 使用 | 当资料增长后，可考虑本地搜索/索引工具辅助查询 |
| Further explorations | 知识库增长后，进一步思考 synthetic data generation 与 fine-tuning | 若 AI-Master 形成稳定高质量语料，可探索训练/微调自己的知识助手 |

## 与当前知识库的关系

AI-Master 当前已经采用 `SCHEMA.md`、`raw/`、`wiki/`、`source-manifest.md`、`index.md`、`log.md` 的结构，本资料可视作该结构的外部方法论来源。后续整理 AI 文章、论文、课程、项目和个人经验时，应优先保证：

- raw 来源可追溯，不随意覆盖；
- wiki 页面要有 frontmatter、tag、sources、wikilink；
- 重要查询和输出要回流，而不是停留在一次性聊天里；
- 定期 lint，及时发现断链、重复页、低置信度内容和 manifest 漂移。

## 待扩展问题

- 什么时候应该只保存 raw，什么时候应该创建 wiki 概念页？
- AI-Master 是否需要独立的“知识库健康检查”操作手册？
- 当资料超过 100 篇、几十万字后，是否需要本地搜索索引、topic map 或 query cache？
- 哪些沉淀内容适合作为 synthetic data 或 fine-tuning 样本？

## Sources

- [LLM Knowledge Bases](../../raw/A_Articles(文章)/I_Important-Articles(重量级文章)/LLM%20Knowledge%20Bases.md)
