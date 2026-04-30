# AI 大师知识库 Schema

## Domain

本知识库用于长期整理所有 AI 相关知识，以及用户自己的学习记录、实践经验、研究观点、方法论和项目沉淀。

范围包括但不限于：
- AI/ML/LLM 基础概念、模型架构、训练、推理、评测、数据、Agent、RAG、工具链与工程实践。
- 论文、文章、课程、书籍、访谈、会议、产品文档等外部资料的原始归档与整理。
- 用户自己的学习笔记、实验记录、项目复盘、经验总结、观点判断、工具使用心得。
- AI 产品、公司、开源项目、模型、框架、平台和行业趋势研究。

## Directory Layout

```text
AI-Master/
  README.md              # 极简入口说明
  SCHEMA.md              # 本文件：结构、标签、写作、raw、Obsidian 规则
  DB/                    # Obsidian Bases：用于卡片视图、资料库筛选和导航
  wiki/                  # 整理层 / 综合层
    index.md
    log.md
    E_Entities(实体)/
    C_Concepts(概念)/
    C_Comparisons(比较)/
    Q_Queries(查询)/
    L_Learning-Notes(学习笔记)/
    E_Experience(经验)/
    O_Opinions(观点)/
    P_Playbooks(操作手册)/
    P_Projects(项目)/
    T_Templates(模板)/
    M_Meta(元信息)/
  raw/                   # 原始资料层，原则上只读、不可随意改写
    source-manifest.md
    A_AI-Gurus(AI大神)/
    A_AI-Content-Creator(AI 创作者)/
    A_Articles(文章)/
    A_Assets(素材)/
      A_Avatar/
    B_Books(书籍)/
    C_Courses(课程)/
    D_Datasets(数据集)/
    E_Experiments(实验)/
    A_AI-Agent-Tech-Stack/
      H_Hermes-Agent/
        T_Tutorials(教程)/
      L_LLM-Wiki/
    P_Papers(论文)/
    P_Prompts(提示词)/
    T_Transcripts(转录)/
```

## Layer Rules

- `raw/` 是原始资料层：保存外部来源、用户原始摘录、PDF/OCR/HTML 导入副本、实验原始输出等。除导入时生成清单/派生 Markdown 外，不随意改写原始来源内容。
- `wiki/` 是整理层：由 AI 助手和用户共同维护，用于综合、抽象、交叉链接、形成可复用知识。
- `SCHEMA.md` 与 `wiki/`、`raw/` 同级，约束整个知识库。
- 从 `wiki/` 子目录页面引用 raw 来源时使用相对路径：通常为 `../../raw/...`；从 `wiki/index.md`、`wiki/log.md` 等 wiki 根文件引用 raw 时使用 `../raw/...`。

## Naming Conventions

- 中文知识、学习、经验、观点类页面优先使用中文文件名，例如 `wiki/C_Concepts(概念)/注意力机制.md`。
- 客观标识可保留英文、模型名、论文名、项目名、日期、版本号，例如 `GPT-4.md`、`Transformer.md`、`2026-04-30-agent实验.md`。
- 不使用拼音简称或拼音全称来代替中文标题。
- 每个 Markdown 页面文件名应稳定、可读、可长期引用。
- `raw/` 和 `wiki/` 下的目录（含子目录）通常采用 `前缀_English(中文)` 格式，例如 `raw/B_Books(书籍)/`；前缀用于排序或分类，英文便于跨工具识别，中文括注便于 Obsidian 中阅读。
- Agent 相关英文术语目录保留英文原名，不额外加中文括注，例如 `raw/A_AI-Agent-Tech-Stack/`、`raw/A_AI-Agent-Tech-Stack/H_Hermes-Agent/`、`raw/A_AI-Agent-Tech-Stack/L_LLM-Wiki/`。

## Page Types

允许的 `type`：
- `entity`：实体页，人、机构、模型、产品、项目、框架、论文、课程等。
- `concept`：概念页，技术概念、方法、理论、术语。
- `comparison`：比较页，模型/框架/方案/观点对比。
- `query`：值得沉淀的问答或专题查询。
- `learning-note`：学习笔记。
- `experience`：实践经验、踩坑记录、工具使用心得。
- `opinion`：用户观点、判断、假设、趋势观察。
- `playbook`：可复用操作手册、流程、方法论。
- `project`：项目页、实验页、构建记录。
- `template`：模板页。
- `summary`：综合总结页。

## Frontmatter

每个 `wiki/` 页面必须以 YAML frontmatter 开头：

```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | learning-note | experience | opinion | playbook | project | template | summary
tags: [taxonomy-tag]
sources: [../../raw/A_Articles(文章)/source.md]
confidence: high | medium | low
---
```

可选字段：

```yaml
contested: true
contradictions: [other-page]
status: evergreen | draft | active | archived
```

## Raw Source Frontmatter

导入到 `raw/` 的 Markdown 派生资料建议带最小 frontmatter：

```yaml
---
source_url: https://example.com/source
ingested: YYYY-MM-DD
sha256: <body_sha256>
source_type: article | paper | book | course | transcript | dataset | experiment | prompt | note
---
```

`sha256` 只计算 frontmatter 之后的正文内容，用于检测原始资料漂移。

## Tag Taxonomy

### AI 基础与模型
- `ai`
- `machine-learning`
- `deep-learning`
- `llm`
- `multimodal`
- `architecture`
- `transformer`
- `agent`
- `rag`
- `reasoning`

### 训练、数据、评测、推理
- `training`
- `fine-tuning`
- `alignment`
- `rlhf`
- `data`
- `evaluation`
- `benchmark`
- `inference`
- `serving`
- `optimization`

### 工程与工具链
- `engineering`
- `mlops`
- `prompt-engineering`
- `tooling`
- `workflow`
- `automation`
- `coding-agent`
- `observability`

### 实体与行业
- `person`
- `model`
- `paper`
- `company`
- `product`
- `open-source`
- `framework`
- `platform`
- `industry`
- `policy`

### 个人学习与沉淀
- `learning-note`
- `experience`
- `opinion`
- `playbook`
- `project`
- `experiment`
- `case-study`
- `mistake`
- `lesson`
- `template`

### 元信息
- `comparison`
- `query`
- `summary`
- `timeline`
- `controversy`
- `glossary`
- `source`

规则：页面使用的所有 tag 必须来自本 taxonomy；如需新增 tag，先修改本文件再使用。

## Page Thresholds

- 当某个实体/概念在 2 个以上来源中出现，或是某个单一来源的核心主题时，可创建页面。
- 对用户自己的经验、观点、项目、实验，只要具有长期复用价值即可创建页面。
- 不为一次性、边缘性、无复用价值的提及创建页面。
- 页面超过约 200 行时，优先拆分为更小主题并互相链接。
- 已被完全替代的页面移动到 `wiki/_archive/`，并从 `index.md` 移除。

## Writing Conventions

- 新页面至少包含 2 个内部 `[[wikilinks]]`，除非当前知识库刚初始化且暂时没有可链接页面。
- 更新页面时必须更新 `updated` 日期。
- 新建或更新页面后，必须同步更新 `wiki/index.md`。
- 每次导入、整理、查询、lint、结构调整，都必须追加 `wiki/log.md`。
- 观点类页面必须区分：事实、推断、个人判断、待验证假设。
- 快速变化或单来源信息默认 `confidence: medium` 或 `low`；多来源稳定事实才使用 `high`。
- 发生冲突时保留两种说法，记录来源和日期，不静默覆盖。

## Suggested Page Structures

### Concept Page

```markdown
# 概念名

## 定义
## 为什么重要
## 核心机制
## 适用场景
## 局限与误区
## 相关概念
## Sources
```

### Learning Note

```markdown
# 学习主题

## 学习来源
## 核心收获
## 关键细节
## 我的理解
## 待复习问题
## 可迁移经验
```

### Experience Page

```markdown
# 经验主题

## 背景
## 问题
## 做法
## 结果
## 踩坑
## 以后怎么做
```

### Opinion Page

```markdown
# 观点主题

## 结论
## 事实依据
## 推理链路
## 反方观点
## 置信度
## 后续验证
```

### Playbook Page

```markdown
# 操作手册

## 适用场景
## 前置条件
## 步骤
## 验证
## 常见问题
## 参考来源
```

## Index Rules

`wiki/index.md` 是总导航。每个 wiki 页面都必须被列入某个栏目，并附一行摘要。

栏目包括：
- Entities
- Concepts
- Comparisons
- Queries
- Learning Notes
- Experience
- Opinions
- Playbooks
- Projects
- Templates
- Meta

当任一栏目超过 50 项时，按主题或首字母拆分；当总页面超过 200 个时，创建 `wiki/M_Meta(元信息)/topic-map.md`。

## Raw Source Rules

- 外部资料导入时，不移动、不删除原始来源目录；只复制到 `raw/` 或记录在 `raw/source-manifest.md`。
- 本地 HTML/MHT/PDF/OCR 导入应保留原始资源副本，并在目标 raw 子目录生成可检索 Markdown 派生文档。
- `raw/source-manifest.md` 记录来源、目标位置、统计、清单和注意事项。
- `raw/A_Assets(素材)/` 保存图片、截图、图表等资源；`wiki/` 页面引用图片时使用相对路径。

## Obsidian Rules

- 本知识库可直接用 Obsidian 打开根目录 `AI-Master/`。
- 使用 Obsidian wikilinks：`[[页面名]]`、`[[页面名#标题]]`、`[[页面名|显示文本]]`。
- 避免依赖插件才能阅读的复杂语法；保持普通 Markdown 可读。
- 若目录为空但需要被 Git 保留，使用空的 `readme.md`，不使用 `.gitkeep`。

## Git Rules

- 本知识库已启用 Git，仓库根目录是 `AI-Master/`，默认分支为 `master`。
- Git 配置：`core.autocrlf=input`，`core.safecrlf=warn`。
- 大规模结构调整、导入、整理后可执行 `git add` 和 `git commit`。
- 不主动 `git push`，除非用户明确要求。
- commit message 使用中文。
- `.gitignore` 忽略 macOS、编辑器、Obsidian workspace/cache、日志、缓存、依赖目录、环境变量等本地状态文件。
- 默认追踪 Markdown、raw 来源文件、assets，以及必要的 Obsidian 配置文件；空目录使用空的 `readme.md` 占位，不使用 `.gitkeep`。

## Update Policy

当新资料与已有内容冲突：
1. 检查来源日期和资料类型。
2. 同时记录旧说法与新说法，注明来源。
3. 必要时在 frontmatter 中设置 `contested: true` 与 `contradictions:`。
4. 在 `wiki/log.md` 标记需要用户复核。

## Lint Expectations

定期检查：
- 断链 wikilinks
- 孤立页面
- index 缺项
- frontmatter 缺字段
- 非 taxonomy tag
- raw source hash 漂移
- 超过 200 行的大页面
- `confidence: low` 或 contested 页面
