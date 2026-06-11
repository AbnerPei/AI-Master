## [2026-04-30] update | 统一 raw 与 wiki 目录命名
- Rule: `raw/` 与 `wiki/` 下目录统一为 `前缀_English(中文)` 格式，例如 `raw/B_Books(书籍)/`。
- Renamed raw directories: `A_AI-Gurus(AI大神)/`、`H_Hermes-Agent(Hermes智能体)/T_Tutorials(教程)/`、`A_Articles(文章)/`、`A_Assets(素材)/`、`B_Books(书籍)/`、`C_Courses(课程)/`、`D_Datasets(数据集)/`、`E_Experiments(实验)/`、`P_Papers(论文)/`、`P_Prompts(提示词)/`、`T_Transcripts(转录)/`。
- Renamed wiki directories: `E_Entities(实体)/`、`C_Concepts(概念)/`、`C_Comparisons(比较)/`、`Q_Queries(查询)/`、`L_Learning-Notes(学习笔记)/`、`E_Experience(经验)/`、`O_Opinions(观点)/`、`P_Playbooks(操作手册)/`、`P_Projects(项目)/`、`T_Templates(模板)/`、`M_Meta(元信息)/`。
- Updated: `SCHEMA.md`、`raw/source-manifest.md`、相关 wiki 页面中的 raw 来源路径。

# AI 大师知识库 Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-05-22] ingest | 补充 YouTube AI 大神 Hung-yi Lee 资料
- Added raw file: `raw/A_AI-Gurus(AI大神)/AI 大神 - Hung-yi Lee.md`。
- Source: YouTube 频道 `https://www.youtube.com/@HungyiLeeNTU`，平台识别为 `YouTube`。
- Updated: `raw/source-manifest.md`，刷新 AI 大神文件数量与文件级 SHA-256。

## [2026-05-30] ingest | 整理 `earendil-works/pi` 项目资料
- Added raw directory: `raw/A_AI-Agent-Tech-Stack/P_Pi/`，包含 `README`、`quickstart`、`extensions`、`skills`、`packages`、`custom providers`、`pi-ai`、`pi-agent-core` 和 `GitHub API` 快照共 `9` 份来源页。
- Added assets: `raw/A_Assets(素材)/P_Pi/`，包含 `3` 张基于 `image-2` 生成的 `Pi` 文档配图。
- Created wiki pages: `wiki/P_Projects(项目)/Pi.md`、`wiki/C_Concepts(概念)/Pi 的可扩展 Agent Harness.md`、`wiki/P_Playbooks(操作手册)/Pi 上手与扩展路线.md`。
- Updated: `wiki/index.md`、`wiki/M_Meta(元信息)/AI 资源索引.md`、`raw/source-manifest.md`。

## [2026-05-19] create | 新增 `OpenSpec` 命令详解与配图操作手册
- Created wiki page: `wiki/P_Playbooks(操作手册)/OpenSpec 命令与使用详解.md`
- Added assets: `raw/A_Assets(素材)/O_OpenSpec/` 下 9 张 `OpenSpec` 主题配图，风格参考来自用户指定的 `image - 2`。
- Purpose: 系统解释 `OpenSpec` 的 `CLI` 命令、`/opsx:*` 工作流命令、实战使用路径、版本差异和常见误区。
- Updated: `wiki/index.md`、`raw/source-manifest.md`

## [2026-05-19] update | 升级 `Codex` `GitHub bounty Agent` 手册为目标驱动型版本
- Updated wiki page: `wiki/P_Playbooks(操作手册)/Codex GitHub bounty Agent 搭建手册.md`
- Change: 从“半自动执行助手”重写为“目标驱动型自主 `Agent`”手册，新增每周 `100` 美元目标拆解、`零资本投入` 边界、机会评分模型、自动回复策略、状态机和高自主系统提示词。

## [2026-05-19] create | 新增 `Codex` `GitHub bounty Agent` 搭建手册
- Created wiki page: `wiki/P_Playbooks(操作手册)/Codex GitHub bounty Agent 搭建手册.md`
- Purpose: 把“如何做一个能自己找 `bounty`、改代码、提 `PR` 的 `Agent`”整理成可执行手册，明确阶段路线、选题规则、执行清单、提示词骨架和一周试运行方案。
- Updated: `wiki/index.md`

## [2026-05-18] ingest | 补充视频号 AI 创作者未来博士wepon资料
- Added raw file: `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 未来博士wepon.md`。
- Source: 微信视频号短链 `https://weixin.qq.com/sph/ArbFUY5yqw`，平台识别为 `视频号`。
- Updated: `raw/source-manifest.md`，刷新 AI 创作者文件数量与文件级 SHA-256。

## [2026-05-17] ingest | 补充视频号 AI 创作者聂风KIKI的创业成长资料
- Added raw file: `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 聂风KIKI的创业成长.md`。
- Source: 微信视频号短链 `https://weixin.qq.com/sph/AAe3RrsrPJ`，平台识别为 `视频号`。
- Updated: `raw/source-manifest.md`，刷新 AI 创作者文件数量与文件级 SHA-256。

## [2026-05-17] create | 新增 `OpenSpec` 安装与使用操作手册
- Created wiki page: `wiki/P_Playbooks(操作手册)/OpenSpec 安装与使用.md`
- Purpose: 记录 `OpenSpec` 的本机安装结果、`Node.js` 版本切换、`Codex` 适配初始化命令和常用 `CLI` 用法。
- Updated: `wiki/index.md`

## [2026-05-17] ingest | 补充视频号 AI 创作者杨彧鑫AI资料
- Added raw file: `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 杨彧鑫AI.md`。
- Source: 微信视频号短链 `https://weixin.qq.com/sph/AKhY3c3eUZ`，平台识别为 `视频号`。
- Updated: `raw/source-manifest.md`，刷新 AI 创作者文件数量与文件级 SHA-256。

## [2026-05-14] ingest | 补充 YouTube AI 创作者秋芝2046资料
- Added raw file: `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 秋芝2046.md`。
- Source: YouTube 频道 `https://www.youtube.com/@qiuzhi2046`，平台识别为 `YouTube`。
- Updated: `raw/source-manifest.md`，刷新 AI 创作者文件数量与文件级 SHA-256。

## [2026-05-12] ingest | 补充视频号 AI 大神傅盛讲AI资料
- Added raw file: `raw/A_AI-Gurus(AI大神)/AI 大神 - 傅盛讲AI.md`。
- Source: 微信视频号短链 `https://weixin.qq.com/sph/At1xESEPjT`，平台识别为 `视频号`。
- Updated: `raw/source-manifest.md`，刷新 AI 大神文件数量与文件级 SHA-256。

## [2026-05-12] update | 时间轴追加微信视频号待整理链接
- Updated file: `Timeline/2026/2026-05 学习时间线.md`。
- Added entry: 新增 `https://weixin.qq.com/sph/At1xESEPjT` 到当天时间轴，先按待整理条目落盘，后续再补内容摘要和个人理解。

## [2026-05-12] update | 切换 `Timeline` 到自定义 `AIHOT` 风格插件
- Updated files: `Timeline/2026/2026-05 学习时间线.md`、`Timeline/模板/学习时间线模板.md`、`Timeline/模板/学习条目模板.md`、`Timeline/时间线使用说明.md`、`SCHEMA.md`。
- Change: 将月文件和模板从旧的 `easy-timeline` / `timeline` 首行元数据写法切换为自定义插件 `timeline` 的 `aihot-timeline` `YAML` 条目语法。
- Updated: `.obsidian/appearance.json`，移除仅服务旧时间线方案的 `时间线卡片纵向布局` `CSS snippet`。

## [2026-05-12] update | 修正 `aihot-timeline` 条目中的 `YAML` 标量写法
- Updated files: `Timeline/2026/2026-05 学习时间线.md`、`Timeline/模板/学习时间线模板.md`、`Timeline/模板/学习条目模板.md`、`Timeline/时间线使用说明.md`。
- Change: 将包含反引号等 `Markdown` 符号的字段值改为带引号的合法 `YAML` 字符串，并将 `tags` 保持为纯文本标签，避免解析失败。

## [2026-05-12] update | 调整 `Timeline` 渲染结构与卡片布局
- Updated files: `Timeline/2026/2026-05 学习时间线.md`、`Timeline/模板/学习时间线模板.md`、`Timeline/模板/学习条目模板.md`、`Timeline/时间线使用说明.md`。
- Added snippet: `.obsidian/snippets/时间线卡片纵向布局.css`，将同日多卡片改为纵向堆叠，并隐藏卡片正文里重复的首行日期元数据。
- Updated: `.obsidian/appearance.json`，启用 `时间线卡片纵向布局` `CSS snippet`。

## [2026-05-12] update | 将 `Timeline` 条目正文改为 `callout`
- Updated files: `Timeline/2026/2026-05 学习时间线.md`、`Timeline/模板/学习时间线模板.md`、`Timeline/模板/学习条目模板.md`、`Timeline/时间线使用说明.md`。
- Change: 将条目正文中的 `笔记`、`摘句`、`我的理解`、`下一步` 改为 `Obsidian callout` 写法，便于在时间线卡片内形成清晰分区。

## [2026-05-12] update | 隐藏时间线首行元数据正文回显
- Updated files: `Timeline/2026/2026-05 学习时间线.md`、`Timeline/模板/学习时间线模板.md`、`Timeline/模板/学习条目模板.md`、`Timeline/时间线使用说明.md`。
- Change: 将时间线首行日期与 `[title::]` / `[icon::]` / `[status::]` 元数据改为 `HTML comment`，避免正文里继续显示 `video`、`success` 等解析辅助字段。

## [2026-05-12] update | 补充 `Timeline` 学习记录
- Updated file: `Timeline/2026/2026-05 学习时间线.md`。
- Added entry: `2026-05-12 06:40` 的 `YouTube` 学习记录，主题是对 `Agent`、简单 `Agent` 创建方式和 `ReAct` 工作模式的初步理解。

## [2026-05-12] create | 新增 Timeline 学习时间线目录
- Added root directory: `Timeline/`，包含 `时间线使用说明.md`、`模板/学习时间线模板.md`、`模板/学习条目模板.md`、`2026/2026-05 学习时间线.md`。
- Configured plugin: 新增 `.obsidian/plugins/easy-timeline/data.json`，将 `easy-timeline` 的参考字段设置为 `创建日期`，默认排序设为 `desc`。
- Updated: `README.md`、`SCHEMA.md`，将 `Timeline/` 纳入知识库结构和使用规则。

## [2026-05-11] update | 将 AI 工具导航收藏改为时间轴卡片呈现
- Updated raw file: `raw/A_Tools(工具)/A_AI-Tool-Directories(AI工具导航)/AI 工具导航与信息源收藏.md`。
- Change: 将原表格改为参考 `AIHOT` 的“日期分组 + 上下时间轴 + 网址卡片 + 推荐理由 + 下一步动作”结构。
- Updated: `raw/source-manifest.md`，刷新正文 SHA-256、文件级 SHA-256、大小和行数。

## [2026-05-11] create | 新增 AI 工具导航与信息源收藏清单
- Added raw directory: `raw/A_Tools(工具)/A_AI-Tool-Directories(AI工具导航)/`。
- Created raw file: `raw/A_Tools(工具)/A_AI-Tool-Directories(AI工具导航)/AI 工具导航与信息源收藏.md`，记录 `AI工具集` 与 `AIHOT` 两个网址。
- Updated: `SCHEMA.md`、`raw/source-manifest.md`，登记目录规则、来源说明和文件级 SHA-256。
- Notes: 当前仅作为 raw 层网址收藏；后续如形成固定工具发现 / 信息监控流程，再整理到 `wiki/P_Playbooks(操作手册)/AI 工具发现与信息监控.md`。


## [2026-05-11] ingest | 补充 Git 工具学习资料与视频号下载教程
- Added raw directory: `raw/A_Tools(工具)/Git/`，包含 Git 教程、链接笔记与配图。
- Added raw course: `raw/C_Courses(课程)/T_Tutorials(教程)/如何下载视频号的视频/`，包含视频号下载教程与截图。
- Added repo note: `AGENTS.md`，记录本仓库 Markdown frontmatter 与 Obsidian 语法约定。
- Updated: `SCHEMA.md`、`raw/source-manifest.md`，登记新增 raw 目录、文件清单、素材 SHA-256 和统计信息。
- Notes: `.obsidian/appearance.json`、`.obsidian/types.json` 与 `.obsidian/snippets/` 记录本次 Obsidian 外观和属性配置更新。

## [2026-05-11] ingest | 补充视频号 AI 创作者张咋啦Zara资料
- Added raw file: `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 张咋啦Zara.md`。
- Source: 微信视频号短链 `https://weixin.qq.com/sph/Av0dEnlvVz`，平台识别为 `视频号`。
- Updated: `raw/source-manifest.md`，刷新 AI 创作者文件数量与文件级 SHA-256。

## [2026-05-05] ingest | 吸收视频号 AI 人物与创作者新增资料
- Added raw files: `raw/A_AI-Gurus(AI大神)/AI 大神 - 李尚龙.md`、`raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 2B大叔.md`、`raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 晓辉博士.md`。
- Added clipping files: `Clippings/视频号/你以为的“贩卖焦虑”只是你没见过的“世界常识”贩卖焦虑.md`、`Clippings/视频号/AU25W7Em6f_meta.json`、`Clippings/视频号/AU25W7Em6f_cover.jpg`。
- Updated: `SCHEMA.md`、`raw/source-manifest.md`、`DB/DB_AI 大神.base`。
- Normalized directory: 将用户新增的 `raw/A_AI-Content-Creator(AI创作者)/` 文件归并到规范路径 `raw/A_AI-Content-Creator(AI 创作者)/`。
- Notes: 本次按用户要求阅读新增改动、补充 manifest/log/schema 记录、提交并 push。

## [2026-05-05] create | 新增个人 AI 思考 raw 目录与 Agent 方法论草稿
- Added raw directory: `raw/M_My-AI-Thoughts(我的AI思考)/`。
- Created raw file: `raw/M_My-AI-Thoughts(我的AI思考)/如何创建、进化和使用自己的 Agent.md`。
- Updated: `SCHEMA.md`、`raw/source-manifest.md`。
- Notes: 本次仅创建 raw 层个人原始思考草稿，围绕如何创建自己的 Agent、如何进化 Agent、如何使用 Agent；暂未创建 wiki 整理页。

## [2026-05-05] ingest | 补充提交 B站 AI 创作者所长林超资料
- Added raw file: `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 所长林超.md`。
- Updated: `raw/source-manifest.md`，刷新 AI 创作者文件数量与文件级 SHA-256。
- Notes: 本次按用户要求补充提交此前未纳入 Git 的新增 AI 创作者资料，并 push 到远程 `origin/master`。

## [2026-05-01] update | 吸收新增 B站 AI 创作者资料并规范目录
- Added raw files: `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - code秘密花园.md`、`raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 慢学AI.md`、`raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 堂吉诃德拉曼查的英豪.md`。
- Updated raw file: `raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - 第四种黑猩猩CHIMP.md`，按用户改动恢复为 B 站头像 URL 引用。
- Created wiki page: `wiki/P_Playbooks(操作手册)/B站 AI 创作者技能快速导入.md`，并更新 `wiki/index.md`。
- Normalized directory: 将误生成的 `raw/A_AI-Content-Creator(AI创作者)/` 文件归并到规范目录 `raw/A_AI-Content-Creator(AI 创作者)/`。
- Updated: `raw/source-manifest.md`，刷新 raw Markdown 与素材 SHA-256、大小和行数。
- Note: 本次按用户要求吸收改动、提交并 push。

## [2026-05-01] create | B站 AI 创作者技能快速导入操作手册
- Created wiki page: `wiki/P_Playbooks(操作手册)/B站 AI 创作者技能快速导入.md`
- Purpose: 记录 `ai-creator-info` 与 `bilibili-up-info` 两个 skill 的软链接恢复、依赖安装、JSON 查询和 md 生成流程。
- Updated: `wiki/index.md`

## [2026-04-30] update | 配置 GitHub 远程仓库并推送 master
- Remote: `origin` -> `git@github.com:AbnerPei/AI-Master.git`
- Branch: 本地分支从 `main` 重命名为 `master`，并设置跟踪 `origin/master`。
- Push: 已执行 `git push -u origin master`。
- Updated: `SCHEMA.md`，将 Git 默认分支记录更新为 `master`。

## [2026-04-30] update | 用户更新 AI 大神与 Hermes Agent raw 资料
- Updated raw files: `raw/A_AI-Gurus(AI大神)/AI 大神 - Andrej Karpathy.md`，`raw/H_Hermes-Agent(Hermes智能体)/T_Tutorials(教程)/Hermes Agent教程 - 接入微信.md`
- Updated: `raw/source-manifest.md`，刷新文件大小、行数和 SHA-256。
- Note: 用户直接修改 raw 文件；本次仅同步 manifest 并提交，不改写整理层 wiki 页面。

## [2026-04-30] ingest | 用户导入 AI 大神与 Hermes Agent 两个 raw 目录
- Raw directories: `raw/A_AI-Gurus(AI大神)/`，`raw/H_Hermes-Agent(Hermes智能体)/`
- Raw Markdown files: 2
- Updated: `raw/source-manifest.md`
- Created wiki pages: `wiki/E_Entities(实体)/Andrej Karpathy.md`，`wiki/E_Entities(实体)/Hermes Agent.md`，`wiki/P_Playbooks(操作手册)/Hermes Agent 接入微信.md`，`wiki/M_Meta(元信息)/AI 资源索引.md`
- Updated: `wiki/index.md`
- Updated: `SCHEMA.md`，在 tag taxonomy 中新增 `person`，用于 AI 人物/专家实体页。
- Note: 未改写用户导入的 raw 文件，仅登记 manifest 并创建整理层页面。

## [2026-04-30] create | 引入 Git 版本管理
- Repository root: `/Users/peijianbo/Documents/MeMe/AI-Master`
- Branch: `main`
- Config: `core.autocrlf=input`，`core.safecrlf=warn`
- Created: `.gitignore`
- Updated: `SCHEMA.md` 的 Git Rules，明确仓库边界、忽略规则、提交规则和不主动 push 规则。

## [2026-04-30] create | 初始化 AI 大师知识库
- Domain: 整理所有 AI 相关知识，以及用户自己的学习、经验、观点、项目和方法论沉淀。
- Structure: 创建知识库根目录、`SCHEMA.md`、`README.md`、`wiki/`、`raw/`、索引、日志和基础分类目录。
- Layout: `SCHEMA.md`、`wiki/`、`raw/` 同级；`wiki/` 为整理层，`raw/` 为原始资料层。

## [2026-04-30] ingest | LLM Knowledge Bases 文章资料
- Source URL: https://x.com/karpathy/status/2039805659525644595
- Author: Andrej Karpathy (@karpathy)
- Published: 2026-04-02T20:42:21Z
- Created raw file: `raw/A_Articles(文章)/I_Important-Articles(重量级文章)/LLM Knowledge Bases.md`
- Created wiki page: `wiki/C_Concepts(概念)/LLM Knowledge Bases.md`
- Updated: `raw/source-manifest.md`、`wiki/index.md`、`wiki/E_Entities(实体)/Andrej Karpathy.md`、`wiki/M_Meta(元信息)/AI 资源索引.md`
- Notes: 按 `前缀_English(中文)` 目录规范新增重量级文章子目录；未 push。
## [2026-04-30] update | 优化 LLM Knowledge Bases raw 正文格式
- Updated raw file: `raw/A_Articles(文章)/I_Important-Articles(重量级文章)/LLM Knowledge Bases.md`
- Removed duplicated body sections already covered by YAML frontmatter: top-level title, `Source Metadata`, `Tags`, `Classification`.
- Added: 中文翻译对照；正文保留 `Original Text` 和 `Local Notes`。
- Updated: `raw/source-manifest.md` 文件大小、行数和 SHA-256；`SCHEMA.md` 记录英文博客/长文导入格式偏好。

## [2026-04-30] ingest | LLM Wiki 详解与 Agent 技术栈目录修正
- Renamed raw directories: `raw/A_AI-Agent-Tech-Stack(AI Agent技术栈)/` -> `raw/A_AI-Agent-Tech-Stack/`，`H_Hermes-Agent(Hermes智能体)/` -> `H_Hermes-Agent/`。
- Created raw doc: `raw/A_AI-Agent-Tech-Stack/L_LLM-Wiki/LLM Wiki 详解.md`
- Created asset: `raw/A_Assets(素材)/L_LLM-Wiki/llm-wiki-workflow.svg`
- Created wiki page: `wiki/C_Concepts(概念)/LLM Wiki.md`
- Updated: `SCHEMA.md`、`raw/source-manifest.md`、`wiki/index.md`、`wiki/M_Meta(元信息)/AI 资源索引.md`、Hermes Agent 相关 wiki 页面来源路径。
- Notes: 图像生成服务缺少 `FAL_KEY`，改为生成可版本管理的本地 SVG 配图；未 push。

## [2026-04-30] update | 修复 LLM Wiki 工作流 SVG 版式
- Updated asset: `raw/A_Assets(素材)/L_LLM-Wiki/llm-wiki-workflow.svg`
- Changes: 四个 workflow item 统一为等宽等高卡片；前 3 个 item 底部说明文字改为居中；底部说明文字下移并加浅色底板，反馈箭头上移，避免重合。
- Updated: `raw/source-manifest.md` 记录 SVG 文件大小与版式修复说明；`.gitignore` 忽略 Obsidian graph 本地状态。
- Notes: 未 push。

## [2026-04-30] update | 记录用户新增 AI 创作者资料与 Obsidian 配置
- Updated raw file: `raw/A_AI-Gurus(AI大神)/AI 大神 - Andrej Karpathy.md`，补充 `AI 创作者` 分类与头像 URL。
- Added raw directory: `raw/A_AI-Content-Creator(AI 创作者)/`，新增 `AI 创作者 - 第四种黑猩猩CHIMP.md`。
- Added asset directory: `raw/A_Assets(素材)/A_Avatar/`，新增 `B站_第四种黑猩猩CHIMP.png`。
- Added Obsidian/Bases files: `DB/DB_AI 创作者.base`、`DB/DB_AI 大神.base`、`.obsidian/bookmarks.json`、`.obsidian/types.json`、`.obsidian/themes/Maple/`；`.obsidian/appearance.json` 切换到 Maple theme。
- Updated: `SCHEMA.md`、`raw/source-manifest.md`。
- Note: 本次按用户要求知晓并提交新增目录/文件；仅修正新增 AI 创作者 raw 文档中的头像相对路径；空白根目录 `未命名.md` 无知识内容，未纳入提交；未 push。
