# Source Manifest

> AI 大师知识库 raw 层来源清单。
> Last updated: 2026-04-30

## Current Raw Layout

- `raw/A_Articles(文章)/`：网页文章、博客、新闻、官方文档摘录。
  - `raw/A_Articles(文章)/I_Important-Articles(重量级文章)/`：对知识库方法论、AI 学习或长期技术判断有持续参考价值的重量级文章。
- `raw/P_Papers(论文)/`：论文、技术报告、arXiv/PDF/OCR 派生材料。
- `raw/B_Books(书籍)/`：书籍摘录、读书原始笔记、章节材料。
- `raw/C_Courses(课程)/`：课程材料、课件、课程字幕、作业资料。
- `raw/T_Transcripts(转录)/`：访谈、播客、会议、视频字幕。
- `raw/D_Datasets(数据集)/`：数据集说明、样例、数据字典。
- `raw/E_Experiments(实验)/`：实验原始记录、日志、结果导出。
- `raw/P_Prompts(提示词)/`：Prompt 原始版本、对话样本、提示词实验。
- `raw/A_Assets(素材)/`：图片、截图、图表、页面渲染图、附件。
- `raw/A_AI-Gurus(AI大神)/`：用户导入的 AI 人物/专家资料。
- `raw/H_Hermes-Agent(Hermes智能体)/`：用户导入的 Hermes Agent 学习与教程资料。

## Placement Rules

- 外部来源目录不移动、不删除；只复制到 `raw/` 或在本清单中记录来源。
- 导入的 Markdown 派生文件应保留来源、导入日期和正文 sha256；对用户已手动放入 `raw/` 的资料，本清单记录文件级 SHA-256，后续如需规范化 frontmatter，应先确认是否允许改写 raw。
- `raw/` 中资料作为 provenance；综合结论写入 `wiki/`。

## Sources

### 用户手动导入 | AI 大神

- Source type: 用户手动导入的本地 Markdown 目录。
- Target: `raw/A_AI-Gurus(AI大神)/`
- Imported/recorded: 2026-04-30
- Last checked: 2026-04-30
- Files: 1 Markdown file。
- Notes: 当前仅记录 raw 文件，不改写原始内容；其中包含 Andrej Karpathy 简介、平台链接与内容链接。

### 用户手动导入 | Hermes Agent

- Source type: 用户手动导入的本地 Markdown 目录。
- Target: `raw/H_Hermes-Agent(Hermes智能体)/`
- Imported/recorded: 2026-04-30
- Last checked: 2026-04-30
- Files: 1 Markdown file。
- Notes: 当前仅记录 raw 文件，不改写原始内容；其中包含 Hermes Agent 接入微信相关参考链接。

### X / Twitter | LLM Knowledge Bases

- Source type: X / Twitter long-form post via public tweet mirror API (`api.fxtwitter.com`) and original X URL。
- Source URL: https://x.com/karpathy/status/2039805659525644595
- Author: Andrej Karpathy (@karpathy)
- Published: 2026-04-02T20:42:21Z
- Target: `raw/A_Articles(文章)/I_Important-Articles(重量级文章)/LLM Knowledge Bases.md`
- Imported/recorded: 2026-04-30
- Last checked: 2026-04-30
- Files: 1 Markdown file。
- Notes: 保存原文、时间、作者、平台、互动数据、tags、分类和本地备注；正文 sha256 写入 raw frontmatter，文件级 SHA-256 写入下方清单。

## File Paths

| Path | Size bytes | Lines | SHA-256 |
|---|---:|---:|---|
| `raw/A_AI-Gurus(AI大神)/AI 大神 - Andrej Karpathy.md` | 836 | 21 | `b0d609d36a954286867cc539ce45d9a5b55d71e1a8adee41d8329c588efbb3ec` |
| `raw/A_Articles(文章)/I_Important-Articles(重量级文章)/LLM Knowledge Bases.md` | 5634 | 87 | `b333f6e580c4ac1e6e6e1401b736730bc32a5d280c4d201b4f8927a73804f35e` |
| `raw/H_Hermes-Agent(Hermes智能体)/T_Tutorials(教程)/Hermes Agent教程 - 接入微信.md` | 316 | 12 | `2b7f19df9245ebd514632963b67a7a7a121d6de5c64ea0731efd4edf3fd372c6` |
