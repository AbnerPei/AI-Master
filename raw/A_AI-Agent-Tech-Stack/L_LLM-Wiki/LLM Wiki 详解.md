---
title: LLM Wiki 详解
ingested: 2026-04-30
sha256: 2ae3950179b1bc04f08b8454e50780f83b5bbe930e513e11d1f8fc076f24be79
source_type: note
source_urls:
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  - https://github.com/atomicmemory/llm-wiki-compiler
  - https://help.obsidian.md/links
  - https://help.obsidian.md/properties
  - https://notes.andymatuschak.org/Evergreen_notes
classification: A_AI-Agent-Tech-Stack/L_LLM-Wiki
---

![LLM Wiki 工作流](../../A_Assets%28素材%29/L_LLM-Wiki/llm-wiki-workflow.svg)

# LLM Wiki 详解

## 1. 一句话定义

LLM Wiki 是一种由 LLM Agent 持续维护的个人或团队知识库模式：所有原始资料先进入 `raw/`，LLM 不只做一次性摘要，而是把资料增量“编译”成结构化、可链接、可维护的 Markdown wiki；后续每次查询、写作、复盘、lint 的结果继续回流到 wiki，使知识像代码库一样不断积累。

它的核心不是“把文件丢给模型问问题”，而是“让模型长期维护一个可阅读、可 diff、可审计、可复用的知识资产”。

## 2. 为什么不是普通 RAG

传统 RAG 的典型流程是：用户提问，系统检索 raw 文档片段，模型临时拼答案。这种方式适合问答，但有几个长期问题：

- 每次提问都要重新发现相关片段，复杂问题容易漏检。
- 多篇资料之间的矛盾、更新、补充关系不会自然沉淀。
- 模型生成的好答案如果不归档，下次仍然要重新推导。
- 原始材料越多，检索结果越依赖 query 写法和 chunk 切分质量。
- 用户很难直接浏览“当前知识结构”，只能不断问模型。

LLM Wiki 的做法是把“检索时临时拼装”前移为“导入时增量编译”：

| 维度 | 普通 RAG | LLM Wiki |
|---|---|---|
| 主要对象 | 向量索引与 chunk | Markdown 页面与 wikilink |
| 工作时机 | 提问时检索 | 导入时整理，提问时复用 |
| 知识状态 | 隐藏在 raw 与索引中 | 显性呈现在 wiki 页面中 |
| 复利能力 | 弱，每次重新综合 | 强，综合结果可持续更新 |
| 人类可读性 | 依赖应用界面 | 文件本身可读、可审查、可 Git 管理 |
| 适合任务 | 快速问答、客服、海量检索 | 长期学习、研究、项目知识、经验沉淀 |

可以把 RAG 理解为“每次从食材临时做饭”，把 LLM Wiki 理解为“建立菜谱、半成品、索引和复盘记录，下次直接升级这套厨房系统”。

## 3. 三层结构

### 3.1 raw：原始资料层

`raw/` 保存外部来源和用户原始材料，例如文章、论文、课程、转录、实验日志、截图、网页存档、PDF OCR 结果等。它的原则是可追溯、尽量不可变。

关键要求：

- 保留来源 URL、导入日期、作者、发布时间、文件哈希等元信息。
- 如果是本地文件导入，只复制到知识库，不移动、不删除源目录。
- raw 资料只作为 provenance，综合判断不要直接写回 raw。
- 重要 raw 子目录需要 `README.md` 或 manifest 说明来源、统计、工具链和局限。
- 对网页、PDF、MHT 等派生 Markdown，要说明正文可能存在 OCR 或编码误差。

### 3.2 wiki：整理层 / 编译层

`wiki/` 是 LLM 维护的知识层。它不是 raw 的简单搬运，而是把来源内容整理成长期可复用页面。

常见页面类型：

- 实体页：人物、公司、模型、产品、框架、项目。
- 概念页：术语、方法、机制、理论、工作流。
- 比较页：模型、工具、方案或观点的横向对比。
- 查询页：值得沉淀的专题问答。
- 操作手册：可重复执行的流程、命令、检查清单。
- 学习笔记：读书、课程、论文、文章的吸收和理解。
- 经验页：实践踩坑、项目复盘、个人方法论。

每个页面都应有 frontmatter、来源、标签和内部链接。好的 wiki 页面不是越长越好，而是能快速回答“这是什么、为什么重要、怎么用、和什么相关、来源在哪里”。

### 3.3 schema：规则层

`SCHEMA.md` 是知识库的“宪法”。它定义：

- 目录结构。
- 文件命名规则。
- 页面类型。
- frontmatter 字段。
- tag taxonomy。
- raw 导入规则。
- Git、Obsidian、更新、lint 规则。

没有 schema，wiki 很快会变成风格不统一的笔记堆；有 schema，LLM 才能在多次会话中保持同一套组织方式。

## 4. 核心工作流

### 4.1 Ingest：导入资料

导入不是复制文件结束，而是一个完整流程：

1. 保存或登记 raw 来源。
2. 计算哈希、记录导入时间和来源信息。
3. 阅读资料，抽取核心实体、概念、观点、事实和争议。
4. 检查现有 `index.md` 和 wiki 页面，避免重复创建。
5. 新建或更新实体页、概念页、比较页、操作手册等。
6. 给重要论断补来源路径，必要时标注置信度和冲突。
7. 更新 `wiki/index.md`、`wiki/log.md` 和 `raw/source-manifest.md`。
8. 验证链接、frontmatter、manifest、Git diff。

### 4.2 Query：查询与专题综合

当用户问一个复杂问题时，LLM 不应该只读 raw，而应先读：

- `SCHEMA.md`：确认规则与领域边界。
- `wiki/index.md`：找到相关页面。
- `wiki/log.md`：理解近期变更。
- 相关实体页、概念页、比较页、查询页。

如果回答本身有长期价值，应沉淀为 `Q_Queries(查询)/` 页面或更新相关概念页。这样下一次同类问题不必重做。

### 4.3 Update：增量更新

当新资料补充旧资料时，不应创建孤立摘要，而应更新已有页面：

- 新事实补到相关实体/概念页。
- 新观点补到观点或比较页。
- 新流程补到 playbook。
- 旧结论被推翻时保留时间线和来源，而不是静默覆盖。
- 页面超过约 200 行时拆分主题页。

### 4.4 Lint：健康检查

LLM Wiki 需要定期 lint，就像代码库需要测试。

重点检查：

- 断掉的 Obsidian 双链。
- 没有入链的孤儿页面。
- index 中漏列的页面。
- frontmatter 缺字段。
- 标签不在 taxonomy 中。
- raw 文件哈希漂移。
- 页面过长、过旧或低置信度。
- `log.md` 是否需要轮转。
- 是否存在敏感字段、密钥或隐私泄漏。

## 5. 页面设计原则

### 5.1 一个页面只承担一个稳定职责

不要把“资料摘要、个人观点、操作步骤、概念定义、项目计划”全部塞进同一个页面。更好的做法是：

- 概念页解释长期稳定的知识。
- 学习笔记记录某次学习来源和理解。
- 经验页记录实践中的判断、失败和教训。
- 操作手册记录可重复流程。
- 查询页记录一次值得保存的综合回答。

### 5.2 先链接，再扩写

LLM Wiki 的价值来自网络，而不是单篇文章。每个新页面至少应该链接两个相关页面；如果暂时没有相关页面，要考虑是否真的值得创建，或是否应该先更新已有页面。

### 5.3 保留来源，不伪装成确定事实

LLM 整理内容时很容易把“某个作者的观点”写成“事实”。更稳妥的写法是：

- 对事实：写清来源与日期。
- 对观点：写清是谁的观点、适用场景和反例。
- 对推断：标注“推断”“假设”“待验证”。
- 对冲突：并列记录不同说法，标注时间线。

### 5.4 让 Obsidian 和 Git 都舒服

好用的 LLM Wiki 应同时满足人读、工具读和版本管理：

- 使用纯 Markdown，避免复杂 HTML 和插件专有语法。
- 内部页面用 Obsidian 双链。
- 图片和 raw 来源用相对路径。
- 每次大改动使用 Git commit。
- index 和 log 保持最新。
- 文件名稳定，不随意改名。

## 6. 适合放进 AI-Master 的内容

AI-Master 的目标是整理所有 AI 相关知识，以及自己的学习、经验、观点。LLM Wiki 很适合作为这个知识库的底层组织方法。

建议把内容分成以下几类：

| 内容类型 | 放置位置 | 说明 |
|---|---|---|
| 外部文章、博客、长帖 | `raw/A_Articles(文章)/` | 保留原文、翻译、来源和哈希 |
| AI 人物与专家资料 | `raw/A_AI-Gurus(AI大神)/` + `wiki/E_Entities(实体)/` | raw 存资料，wiki 存人物画像和观点索引 |
| Agent 工具栈资料 | `raw/A_AI-Agent-Tech-Stack/` | Hermes、LLM Wiki、Claude Code、Codex 等 |
| 论文 | `raw/P_Papers(论文)/` + `wiki/C_Concepts(概念)/` | raw 存论文/OCR，wiki 存机制与结论 |
| 课程与书籍 | `raw/C_Courses(课程)/`、`raw/B_Books(书籍)/` | 章节笔记沉淀到 learning notes |
| 实践经验 | `wiki/E_Experience(经验)/` | 命令、踩坑、排障、经验判断 |
| 观点判断 | `wiki/O_Opinions(观点)/` | 明确区分事实、推断和待验证假设 |
| 操作流程 | `wiki/P_Playbooks(操作手册)/` | 可复用步骤和检查清单 |

## 7. LLM Wiki 与 AI Agent 的关系

LLM Wiki 特别适合与 CLI Agent、Coding Agent、研究 Agent 配合，因为它把“Agent 的工作结果”变成长期文件资产。

常见协作模式：

1. 人提供来源和目标。
2. Agent 定向读取 schema/index/log。
3. Agent 导入 raw 或读取已有 raw。
4. Agent 创建/更新 wiki 页面。
5. Agent 运行验证脚本或 lint。
6. Agent 提交 Git commit。
7. 人在 Obsidian 或编辑器里检查、补充、继续追问。

这种模式下，Obsidian 像 IDE，LLM Agent 像程序员，wiki 像代码库，raw 像测试夹具和来源数据。

## 8. 常见错误

### 8.1 只做摘要，不更新网络

如果每篇文章都生成一个孤立摘要，最后得到的是“摘要坟场”。正确做法是把摘要拆解并合并到已有实体、概念、比较和操作页中。

### 8.2 不读 index 和 log 就开始写

这会导致重复页面、错过已有上下文、破坏命名规则。每次会话开始都应读取 `SCHEMA.md`、`wiki/index.md` 和最近 `wiki/log.md`。

### 8.3 raw 和 wiki 混在一起

raw 是来源，wiki 是综合。如果把来源、判断和后续修订混在同一个文件里，将很难追溯哪些是原文，哪些是后来理解。

### 8.4 过度自动化

LLM Wiki 不等于完全自动写百科。人仍然要决定：哪些来源重要、哪些问题值得追、哪些结论需要保守、哪些页面应归档或重构。

### 8.5 不做 lint

不 lint 的 wiki 会逐渐出现断链、标签膨胀、重复页、低置信度结论、manifest 漂移。越早建立 lint 习惯，后期维护成本越低。

## 9. 推荐实践清单

- 每个知识库都要有 `SCHEMA.md`。
- `SCHEMA.md`、`wiki/`、`raw/` 在项目根目录同级。
- `wiki/index.md` 是入口导航，所有页面都应列入。
- `wiki/log.md` 记录每次导入、更新、查询、lint、迁移。
- raw 文件保留来源、导入日期和哈希。
- 重要 wiki 页面至少两个内部链接。
- 新 tag 先写进 taxonomy，再用于页面。
- 大改动后运行验证，并提交 Git commit。
- 不主动 push，除非用户明确要求。
- 对用户手动放入的来源目录，只复制或登记，不移动、不删除。

## 10. 入门路径

如果从零开始建设一个 LLM Wiki，可以按以下顺序：

1. 明确知识库领域和边界。
2. 创建 `SCHEMA.md`、`wiki/index.md`、`wiki/log.md`、`raw/source-manifest.md`。
3. 先导入 3-5 个高价值来源，而不是海量导入。
4. 为核心实体和概念创建第一批页面。
5. 建立 index 和 log 的更新习惯。
6. 对第一个复杂查询创建 `Q_Queries(查询)/` 页面。
7. 第一次 lint，修复断链、孤儿页和标签问题。
8. 形成稳定流程后再批量导入资料。

## 11. 参考资料

- Andrej Karpathy, “LLM Wiki” gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- atomicmemory / llm-wiki-compiler: https://github.com/atomicmemory/llm-wiki-compiler
- Obsidian Help, Internal links: https://help.obsidian.md/links
- Obsidian Help, Properties: https://help.obsidian.md/properties
- Andy Matuschak, Evergreen notes: https://notes.andymatuschak.org/Evergreen_notes

## 12. Local Notes

- 对 AI-Master 来说，LLM Wiki 不是一个孤立主题，而是整个知识库的维护方法论。
- 后续可以为 AI-Master 增加专门的 lint playbook、query filing playbook、raw import playbook。
- 当 AI-Master 的页面超过 100 篇时，应建立 `_meta/topic-map.md` 或更细的导航层。
- 这篇文档放在 `raw/A_AI-Agent-Tech-Stack/L_LLM-Wiki/`，作为 LLM Wiki 方法论资料和本知识库实践说明；综合导航页见 `wiki/C_Concepts(概念)/LLM Wiki.md`。
