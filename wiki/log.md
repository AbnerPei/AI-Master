# AI 大师知识库 Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

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
