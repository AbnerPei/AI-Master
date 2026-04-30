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
- Updated raw files: `raw/AI 大神/AI 大神 - Andrej Karpathy.md`，`raw/Hermes Agent/Hermes Agent教程/Hermes Agent教程 - 接入微信.md`
- Updated: `raw/source-manifest.md`，刷新文件大小、行数和 SHA-256。
- Note: 用户直接修改 raw 文件；本次仅同步 manifest 并提交，不改写整理层 wiki 页面。

## [2026-04-30] ingest | 用户导入 AI 大神与 Hermes Agent 两个 raw 目录
- Raw directories: `raw/AI 大神/`，`raw/Hermes Agent/`
- Raw Markdown files: 2
- Updated: `raw/source-manifest.md`
- Created wiki pages: `wiki/entities/Andrej Karpathy.md`，`wiki/entities/Hermes Agent.md`，`wiki/playbooks/Hermes Agent 接入微信.md`，`wiki/_meta/AI 资源索引.md`
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
