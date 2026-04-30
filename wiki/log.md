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
