# Source Manifest

> AI 大师知识库 raw 层来源清单。
> Last updated: 2026-05-11

## Current Raw Layout

- `raw/A_Articles(文章)/`：网页文章、博客、新闻、官方文档摘录。
  - `raw/A_Articles(文章)/I_Important-Articles(重量级文章)/`：对知识库方法论、AI 学习或长期技术判断有持续参考价值的重量级文章。
- `raw/A_Tools(工具)/`：工具链、开发工具、命令行、版本管理等原始学习资料。
  - `raw/A_Tools(工具)/A_AI-Tool-Directories(AI工具导航)/`：AI 工具导航、信息源入口、工具发现与监控网址收藏。
  - `raw/A_Tools(工具)/Git/`：Git 学习资料、操作教程、相关链接与配图。
- `raw/P_Papers(论文)/`：论文、技术报告、arXiv/PDF/OCR 派生材料。
- `raw/B_Books(书籍)/`：书籍摘录、读书原始笔记、章节材料。
- `raw/C_Courses(课程)/`：课程材料、课件、课程字幕、作业资料。
  - `raw/C_Courses(课程)/T_Tutorials(教程)/`：操作类课程或教程原始资料。
- `raw/T_Transcripts(转录)/`：访谈、播客、会议、视频字幕。
- `raw/D_Datasets(数据集)/`：数据集说明、样例、数据字典。
- `raw/E_Experiments(实验)/`：实验原始记录、日志、结果导出。
- `raw/P_Prompts(提示词)/`：Prompt 原始版本、对话样本、提示词实验。
- `raw/A_Assets(素材)/`：图片、截图、图表、页面渲染图、附件。
  - `raw/A_Assets(素材)/L_LLM-Wiki/`：LLM Wiki 介绍与方法论文档配图，当前包含 `llm-wiki-workflow.svg`（6516 bytes）。
  - `raw/A_Assets(素材)/A_Avatar/`：人物、创作者、账号等头像图片素材。
- `raw/A_AI-Gurus(AI大神)/`：用户导入的 AI 人物/专家资料。
- `raw/A_AI-Content-Creator(AI 创作者)/`：用户导入的 AI 内容创作者、频道、博主等资料。
- `raw/M_My-AI-Thoughts(我的AI思考)/`：用户关于 AI 的个人原始思考、临时观点草稿、方法论雏形；成熟后可整理到 `wiki/`。
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
- Last checked: 2026-05-05
- Files: 2 Markdown files。
- Notes: 当前仅记录 raw 文件，不改写原始内容；其中包含 Andrej Karpathy、李尚龙等 AI 人物/专家资料。本次用户补充了视频号来源的李尚龙资料。

### 用户手动导入 | AI 创作者

- Source type: 用户手动导入的本地 Markdown 目录与头像素材。
- Target: `raw/A_AI-Content-Creator(AI 创作者)/`
- Asset target: `raw/A_Assets(素材)/A_Avatar/`
- Imported/recorded: 2026-04-30
- Last checked: 2026-05-11
- Files: 8 Markdown files + 1 PNG asset。
- Notes: 当前仅记录 raw 文件与素材，不改写原始内容；包含“第四种黑猩猩CHIMP”、`code秘密花园`、`慢学AI`、`堂吉诃德拉曼查的英豪`、`所长林超`、`张咋啦Zara`、`2B大叔`、`晓辉博士` 等 AI 创作者资料。已将误生成的 `raw/A_AI-Content-Creator(AI创作者)/` 归并到规范路径 `raw/A_AI-Content-Creator(AI 创作者)/`。

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

### 用户原始思考 | 如何创建、进化和使用自己的 Agent

- Source type: 用户口述核心问题后整理的本地 Markdown 原始思考草稿。
- Target: `raw/M_My-AI-Thoughts(我的AI思考)/如何创建、进化和使用自己的 Agent.md`
- Imported/recorded: 2026-05-05
- Last checked: 2026-05-05
- Files: 1 Markdown file。
- Notes: 围绕“如何创建自己的 Agent、怎么进化这个 Agent、怎么用这个 Agent”展开，当前保留在 raw 层作为个人 AI 思考草稿；后续可拆分为 wiki 观点页、操作手册或概念页。

### 视频号剪藏 | 李尚龙

- Source type: 用户快速采集的视频号剪藏，包含 Markdown 摘要、JSON 元数据与封面图。
- Target: `Clippings/视频号/`
- Imported/recorded: 2026-05-05
- Last checked: 2026-05-05
- Files: 1 Markdown file + 1 JSON metadata file + 1 JPG cover image。
- Notes: 当前保留为根目录 `Clippings/` 下的临时剪藏原始落地文件；其中人物资料已另存为 `raw/A_AI-Gurus(AI大神)/AI 大神 - 李尚龙.md`。


### 用户手动记录 | AI 工具导航与信息源收藏

- Source type: 用户手动记录的网址收藏清单。
- Source URLs:
  - https://ai-bot.cn/#term-97
  - https://aihot.virxact.com
- Target: `raw/A_Tools(工具)/A_AI-Tool-Directories(AI工具导航)/AI 工具导航与信息源收藏.md`
- Imported/recorded: 2026-05-11
- Last checked: 2026-05-11
- Files: 1 Markdown file。
- Notes: 当前作为 raw 层网址收藏与候选信息源清单，采用按日期分组的上下时间轴卡片样式；后续如形成固定工具发现 / 信息监控流程，可整理到 `wiki/P_Playbooks(操作手册)/AI 工具发现与信息监控.md`。

### 用户手动导入 | Git 工具学习资料

- Source type: 用户手动导入的本地 Markdown 教程、链接笔记与 PNG 配图。
- Target: `raw/A_Tools(工具)/Git/`
- Asset target: `raw/A_Tools(工具)/Git/Assets/`
- Imported/recorded: 2026-05-11
- Last checked: 2026-05-11
- Files: 6 Markdown files + 6 PNG assets。
- Notes: 当前保留为 raw 层工具学习资料；包含 `git tag`、`git rebase`、`Git` 三种状态、`commit` 后撤销占位、多账号 `GitHub` 参考链接和相关链接。后续如沉淀为可复用流程，可拆分到 `wiki/P_Playbooks(操作手册)/`。

### 用户手动导入 | 视频号下载教程

- Source type: 用户手动导入的本地 Markdown 教程与截图。
- Target: `raw/C_Courses(课程)/T_Tutorials(教程)/如何下载视频号的视频/`
- Imported/recorded: 2026-05-11
- Last checked: 2026-05-11
- Files: 1 Markdown file + 4 PNG assets。
- Notes: 当前保留为 raw 层教程资料；内容记录 `wx_channels_download` 的平台、原理、安装与使用步骤。

## File Paths

| Path | Size bytes | Lines | SHA-256 |
|---|---:|---:|---|
| `raw/A_Tools(工具)/A_AI-Tool-Directories(AI工具导航)/AI 工具导航与信息源收藏.md` | 3345 | 101 | `4510dff1df550e3f47e4009d4d67adb3a9fd88990c86a268d8faeddb0276360a` |
| `raw/A_Tools(工具)/Git/GitHub/在一台电脑上同时使用多个GitHub账号.md` | 173 | 5 | `6fbae1318ad0e584dfb35f337432afc597e817662fcb84b6e3b20af5f9947157` |
| `raw/A_Tools(工具)/Git/Git的三种状态（必须掌握）.md` | 710 | 13 | `19baf235894fc8c03cc405215885099659045392849764ecf3ccd9f98531ef72` |
| `raw/A_Tools(工具)/Git/git commit后撤销.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/A_Tools(工具)/Git/git rebase 详解.md` | 16301 | 722 | `72f38f1801bf63d75276007841f4ce44482546ffa1a2d1e149ccc321d3f001d7` |
| `raw/A_Tools(工具)/Git/git tag 详解.md` | 15286 | 785 | `cc8d8b71d58aa4d1d53e57569a0da3b2e9f50abd050c0e939b2d3f377948e85a` |
| `raw/A_Tools(工具)/Git/git 相关链接.md` | 56 | 5 | `4388f367c38904dd70b52868e278c6f843d7def9494297e69a6bf7fac2a5dd52` |
| `raw/C_Courses(课程)/T_Tutorials(教程)/如何下载视频号的视频/如何下载视频号的视频.md` | 1622 | 58 | `041229f98be96411e12177476fb6c3ff4e73b4d7cddea972af088c2ffd4b9618` |
| `raw/A_AI-Agent-Tech-Stack/H_Hermes-Agent/T_Tutorials(教程)/Hermes Agent教程 - 接入微信.md` | 316 | 12 | `2b7f19df9245ebd514632963b67a7a7a121d6de5c64ea0731efd4edf3fd372c6` |
| `raw/A_AI-Agent-Tech-Stack/L_LLM-Wiki/LLM Wiki 详解.md` | 12625 | 274 | `da22c1753f6b2d722d8101b819f2796537e9ba545fa98d8b34350d5590cf3a17` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 2B大叔.md` | 1102 | 19 | `23dbe3c85315aea82242eeac86b28d27d6befa7ac0065d54f2b5aeac96f48d1a` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - code秘密花园.md` | 440 | 17 | `3b5c82282f1a6b0af9758bd89ee391504a1e72d5f3426b3611f04a9430f16460` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 堂吉诃德拉曼查的英豪.md` | 423 | 17 | `f6fbaa8b3bdf48cb47a06a1fb440e2439e271bfdd09b1437d10c468246930e3d` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 慢学AI.md` | 571 | 17 | `e133677b4ed23904b4d77ebb4e7614cbf891508e35111b246e5bc622dc61bc91` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 所长林超.md` | 482 | 17 | `6ee2d36deea6674f7b24221fb1acaef2edccd78a1c91a4774160f0b07f31402d` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 张咋啦Zara.md` | 751 | 19 | `a2878d56b7d578076919961fb4553bc2901cd0b16acae688a63fe3817a0c8772` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 晓辉博士.md` | 1185 | 19 | `516c723c47bcd975143b902f03c5e53416998c928ff918656997b2be85a95dc9` |
| `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 第四种黑猩猩CHIMP.md` | 593 | 17 | `e334621aed67c3ad44440a39e172b36fd3976fd33661b2e5898a3c6373560ccf` |
| `raw/A_AI-Gurus(AI大神)/AI 大神 - Andrej Karpathy.md` | 903 | 23 | `f6ecdd47d63dd52ae187c456dbc9485861a7541dbfeb06efb1f3565f7b89271e` |
| `raw/A_AI-Gurus(AI大神)/AI 大神 - 李尚龙.md` | 746 | 19 | `afc1e8b6264441bc277e0f71f02cb882fd7cbab6c2cbcbcbf76ba09e58ddc39a` |
| `raw/A_Articles(文章)/I_Important-Articles(重量级文章)/LLM Knowledge Bases.md` | 8140 | 81 | `f3d1e1e9ba4dbdc292b5bc57ae58252d1e637184686db40cfb0b8a155c3f361f` |
| `raw/A_Articles(文章)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/A_Assets(素材)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/B_Books(书籍)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/C_Courses(课程)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/D_Datasets(数据集)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/E_Experiments(实验)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/M_My-AI-Thoughts(我的AI思考)/如何创建、进化和使用自己的 Agent.md` | 13787 | 375 | `ce659727eef864b0a5c2da5c8fc8057840ff20eac2d37918f52397eb193df121` |
| `raw/P_Papers(论文)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/P_Prompts(提示词)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw/T_Transcripts(转录)/readme.md` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Asset Paths

| Path | Size bytes | SHA-256 |
|---|---:|---|
| `raw/A_Tools(工具)/Git/Assets/Rebase/git-rebase-interactive.png` | 988634 | `a99f10b49520edab9e3061fcfa2bde86df6c0dad256daf0e7c379cc40656291c` |
| `raw/A_Tools(工具)/Git/Assets/Rebase/git-rebase-vs-merge.png` | 1122805 | `15a416c8d8c60702310e316f2a91a27daeb7faeff3a87fbe01b52d96aa925cd6` |
| `raw/A_Tools(工具)/Git/Assets/Rebase/git-rebase-why.png` | 1031063 | `583939af5021d68af6ca63b2f83702e88535dba30197b8b6eac9a6c447b06c76` |
| `raw/A_Tools(工具)/Git/Assets/Tag/git-tag-release-workflow.png` | 1177729 | `0b5ce6c9432dacb2e84e71b1c9b08e1bebf4d65ae1823c0bcd5b3479be8863cf` |
| `raw/A_Tools(工具)/Git/Assets/Tag/git-tag-types.png` | 1020993 | `acafb980a37a1d9f738a64ec88c54cec5e5872fdc120c4c4f4087d654c21f617` |
| `raw/A_Tools(工具)/Git/Assets/Tag/git-tag-why.png` | 990025 | `fc975491ae75195db4d4ed1e5192515e2ef34b29dc8cec424b42ea6efd97de65` |
| `raw/C_Courses(课程)/T_Tutorials(教程)/如何下载视频号的视频/images/wx_channel_video_001.png` | 240918 | `1d97585299b1803a68d3ac033ca31f8a9979aa2deeaaac39e3a50cf86cba2b43` |
| `raw/C_Courses(课程)/T_Tutorials(教程)/如何下载视频号的视频/images/wx_channel_video_002.png` | 685285 | `31f3b5b7ce923095351e4c5319c72368816f727838c587103447e209d191179a` |
| `raw/C_Courses(课程)/T_Tutorials(教程)/如何下载视频号的视频/images/wx_channel_video_003.png` | 70118 | `00b4529d5e81a97658542f4ce16cf2ffdf391fdac25e11559e51d67d89b984c6` |
| `raw/C_Courses(课程)/T_Tutorials(教程)/如何下载视频号的视频/images/wx_channel_video_004.png` | 275444 | `ff4fbc691c46e4627bd912b44353993312c36cb8fe7207d81f55b1e4a8af764c` |
| `Clippings/视频号/AU25W7Em6f_cover.jpg` | 44622 | `9ada47eada3ae97115dd14e93b95f186a3cdcb545197574b1a8688254739f8c2` |
| `raw/A_Assets(素材)/A_Avatar/B站_第四种黑猩猩CHIMP.png` | 164695 | `5e5d1b69d62baff1262f521ab2333d14e5d127732d4b817112e6304a852bca51` |
| `raw/A_Assets(素材)/L_LLM-Wiki/llm-wiki-workflow.svg` | 6516 | `44e7e2124d0c88dfe14b7b7026e81ec19aa1580b5bdfa877abded21195a3799f` |

## Clipping Metadata Paths

| Path | Size bytes | Lines | SHA-256 |
|---|---:|---:|---|
| `Clippings/视频号/AU25W7Em6f_meta.json` | 966 | 9 | `5cabdb30a140747b76c6e87642d9af65249c0fefcabaa9a325b0b7f21ad77e5c` |
| `Clippings/视频号/你以为的“贩卖焦虑”只是你没见过的“世界常识”贩卖焦虑.md` | 598 | 19 | `f0789113afc64adf6f41567017d050deaeaf14de402f5a36a2477890623363b3` |
