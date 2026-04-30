# Source Manifest

> AI 大师知识库 raw 层来源清单。
> Last updated: 2026-05-01

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
  - `raw/A_Assets(素材)/L_LLM-Wiki/`：LLM Wiki 介绍与方法论文档配图，当前包含 `llm-wiki-workflow.svg`（6516 bytes）。
  - `raw/A_Assets(素材)/A_Avatar/`：人物、创作者、账号等头像图片素材。
- `raw/A_AI-Gurus(AI大神)/`：用户导入的 AI 人物/专家资料。
- `raw/A_AI-Content-Creator(AI 创作者)/`：用户导入的 AI 内容创作者、频道、博主等资料。
- `raw/A_AI-Agent-Tech-Stack/`：AI Agent 技术栈资料；Agent 相关英文术语目录保留英文原名，不加中文括注。
  - `raw/A_AI-Agent-Tech-Stack/H_Hermes-Agent/`：Hermes Agent 学习与教程资料。
  - `raw/A_AI-Agent-Tech-Stack/L_LLM-Wiki/`：LLM Wiki 方法论、教程、参考资料和本知识库实践说明。

## Placement Rules

- 外部来源目录不移动、不删除；只复制到 `raw/` 或在本清单中记录来源。
- 导入的 Markdown 派生文件应保留来源、导入日期和正文 sha256；对用户已手动放入 `raw/` 的资料，本清单记录文件级 SHA-256，后续如需规范化 frontmatter，应先确认是否允许改写 raw。
- `raw/` 中资料作为 provenance；综合结论写入 `wiki/`。
- Agent 相关英文术语目录保持英文原名，例如 `A_AI-Agent-Tech-Stack`、`H_Hermes-Agent`、`L_LLM-Wiki`。

## Sources

### 用户手动导入 | AI 大神

- Source type: 用户手动导入的本地 Markdown 目录。
- Target: `raw/A_AI-Gurus(AI大神)/`
- Imported/recorded: 2026-04-30
- Last checked: 2026-04-30
- Files: 1 Markdown file。
- Notes: 当前仅记录 raw 文件，不改写原始内容；其中包含 Andrej Karpathy 简介、平台链接与内容链接。本次用户补充了 `AI 创作者` 分类与头像 URL 元数据。

### 用户手动导入 | AI 创作者

- Source type: 用户手动导入的本地 Markdown 目录与头像素材。
- Target: `raw/A_AI-Content-Creator(AI 创作者)/`
- Asset target: `raw/A_Assets(素材)/A_Avatar/`
- Imported/recorded: 2026-04-30
- Last checked: 2026-05-01
- Files: 4 Markdown files + 1 PNG asset。
- Notes: 当前仅记录 raw 文件与素材，不改写原始内容；包含“第四种黑猩猩CHIMP”、`code秘密花园`、`慢学AI`、`堂吉诃德拉曼查的英豪` 等 B 站 AI 创作者资料。已将误生成的 `raw/A_AI-Content-Creator(AI创作者)/` 归并到规范路径 `raw/A_AI-Content-Creator(AI 创作者)/`。

### 用户手动导入 | Hermes Agent

- Source type: 用户手动导入的本地 Markdown 目录。
- Target: `raw/A_AI-Agent-Tech-Stack/H_Hermes-Agent/`
- Imported/recorded: 2026-04-30
- Last checked: 2026-04-30
- Files: 1 Markdown file。
- Notes: 当前仅记录 raw 文件，不改写原始内容；其中包含 Hermes Agent 接入微信相关参考链接。已按 Agent 英文术语命名偏好放置在当前路径。

### X / Twitter | LLM Knowledge Bases

- Source type: X / Twitter long-form post via public tweet mirror API (`api.fxtwitter.com`) and original X URL。
- Source URL: https://x.com/karpathy/status/2039805659525644595
- Author: Andrej Karpathy (@karpathy)
- Published: 2026-04-02T20:42:21Z
- Target: `raw/A_Articles(文章)/I_Important-Articles(重量级文章)/LLM Knowledge Bases.md`
- Imported/recorded: 2026-04-30
- Last checked: 2026-04-30
- Files: 1 Markdown file。
- Notes: 元数据保存在 YAML frontmatter；正文保留 Original Text、中文翻译和 Local Notes，避免重复 Source Metadata/Tags/Classification；正文 sha256 写入 raw frontmatter，文件级 SHA-256 写入下方清单。

### 综合整理 | LLM Wiki 详解

- Source type: 基于公开参考资料和 AI-Master 本地实践整理的 Markdown 方法论文档。
- Reference URLs:
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  - https://github.com/atomicmemory/llm-wiki-compiler
  - https://help.obsidian.md/links
  - https://help.obsidian.md/properties
  - https://notes.andymatuschak.org/Evergreen_notes
- Target: `raw/A_AI-Agent-Tech-Stack/L_LLM-Wiki/LLM Wiki 详解.md`
- Asset: `raw/A_Assets(素材)/L_LLM-Wiki/llm-wiki-workflow.svg`
- Imported/recorded: 2026-04-30
- Last checked: 2026-04-30
- Files: 1 Markdown file + 1 SVG asset。
- Notes: 文档系统解释 LLM Wiki 的定义、RAG 差异、raw/wiki/schema 分层、ingest/query/lint 工作流、页面设计原则和 AI-Master 落地方式；SVG 已调整为四个等宽等高 item、居中文案与避让反馈箭头。

## File Paths

| Path | Size bytes | Lines | SHA-256 |
|---|---:|---:|---|
| `raw/A_AI-Agent-Tech-Stack/H_Hermes-Agent/T_Tutorials(教程)/Hermes Agent教程 - 接入微信.md` | 316 | 12 | `2b7f19df9245ebd514632963b67a7a7a121d6de5c64ea0731efd4edf3fd372c6` |
| `raw/A_AI-Agent-Tech-Stack/L_LLM-Wiki/LLM Wiki 详解.md` | 12625 | 274 | `da22c1753f6b2d722d8101b819f2796537e9ba545fa98d8b34350d5590cf3a17` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - code秘密花园.md` | 440 | 17 | `3b5c82282f1a6b0af9758bd89ee391504a1e72d5f3426b3611f04a9430f16460` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 堂吉诃德拉曼查的英豪.md` | 423 | 17 | `f6fbaa8b3bdf48cb47a06a1fb440e2439e271bfdd09b1437d10c468246930e3d` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 慢学AI.md` | 571 | 17 | `e133677b4ed23904b4d77ebb4e7614cbf891508e35111b246e5bc622dc61bc91` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 第四种黑猩猩CHIMP.md` | 593 | 17 | `e334621aed67c3ad44440a39e172b36fd3976fd33661b2e5898a3c6373560ccf` |
| `raw/A_AI-Gurus(AI大神)/AI 大神 - Andrej Karpathy.md` | 903 | 23 | `f6ecdd47d63dd52ae187c456dbc9485861a7541dbfeb06efb1f3565f7b89271e` |
| `raw/A_Articles(文章)/I_Important-Articles(重量级文章)/LLM Knowledge Bases.md` | 8140 | 81 | `f3d1e1e9ba4dbdc292b5bc57ae58252d1e637184686db40cfb0b8a155c3f361f` |
| `raw/A_Articles(文章)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/A_Assets(素材)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/B_Books(书籍)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/C_Courses(课程)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/D_Datasets(数据集)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/E_Experiments(实验)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/P_Papers(论文)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/P_Prompts(提示词)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/T_Transcripts(转录)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Asset Paths

| Path | Size bytes | SHA-256 |
|---|---:|---|
| `raw/A_Assets(素材)/A_Avatar/B站_第四种黑猩猩CHIMP.png` | 164695 | `5e5d1b69d62baff1262f521ab2333d14e5d127732d4b817112e6304a852bca51` |
| `raw/A_Assets(素材)/L_LLM-Wiki/llm-wiki-workflow.svg` | 6516 | `44e7e2124d0c88dfe14b7b7026e81ec19aa1580b5bdfa877abded21195a3799f` |
