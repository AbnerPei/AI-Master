# 在 Claude Code 中使用 OpenSpec

> 基于 StockMaster 项目的实际配置与使用经验整理。

## 什么是 OpenSpec

OpenSpec 是一套 **spec 驱动的变更管理框架**，帮助 AI Agent（Claude Code、Codex、Cursor 等）以结构化、可追溯的方式完成开发工作。它将每次开发工作组织成一个 **Change（变更）**，每个 Change 包含完整的 proposal、design、specs、tasks 四件套。

- **官网**：https://github.com/Fission-AI/OpenSpec
- **当前版本**：v1.3.1（通过 mise 管理，路径 `~/.local/share/mise/shims/openspec`）
- **工作流 Schema**：spec-driven（proposal → specs → design → tasks）

---

## 目录结构

```
项目根目录/
├── openspec/
│   ├── config.yaml          # 工作流配置（schema: spec-driven）
│   ├── changes/             # 活跃变更
│   │   ├── <变更名>/
│   │   │   ├── .openspec.yaml   # 元信息
│   │   │   ├── proposal.md      # 「为什么」— 变更动机与内容
│   │   │   ├── design.md        # 「怎么做」— 上下文、决策、风险、迁移计划
│   │   │   ├── tasks.md         # 实施任务清单（checkbox）
│   │   │   └── specs/           # Delta Specs — 本次变更的规格增量
│   │   └── archive/             # 已归档变更
│   └── specs/                # 地面真相 / 能力规格库（主 specs）
├── .claude/
│   ├── skills/               # Claude Code Skills（SKILL.md）
│   │   ├── openspec-propose/
│   │   ├── openspec-explore/
│   │   ├── openspec-apply-change/
│   │   └── openspec-archive-change/
│   └── commands/opsx/        # 斜杠命令
│       ├── propose.md
│       ├── explore.md
│       ├── apply.md
│       └── archive.md
└── AGENTS.md                 # Agent 规则（含 OpenSpec 特定规则）
```

---

## 安装与配置

### 1. 安装 OpenSpec CLI

```bash
# 通过 npm 全局安装
npm install -g @fission-ai/openspec

# 或通过 mise 管理（推荐）
mise install openspec
```

### 2. 在项目中初始化

```bash
# 初始化 OpenSpec（会检测 .claude 目录并配置 Claude Code）
openspec init --tools claude

# 如果已有 .trae、.codex 等 agent 目录，可同时配置多个
openspec init --tools claude,codex,trae
```

执行后会在 `.claude/` 下生成：
- `skills/` — 4 个 Skill 定义文件（`openspec-propose`、`openspec-explore`、`openspec-apply-change`、`openspec-archive-change`）
- `commands/opsx/` — 4 个斜杠命令（`/opsx:propose`、`/opsx:explore`、`/opsx:apply`、`/opsx:archive`）

### 3. 配置 Delivery 模式

```bash
# 查看当前配置
openspec config list

# 同时生成 skills 和 commands（推荐）
openspec config set delivery both

# 只生成 skills（斜杠命令不会出现在 IDE 中）
openspec config set delivery skills

# 只生成 commands
openspec config set delivery commands
```

### 4. 更新已有配置

当项目新增 agent 工具目录时：

```bash
openspec update          # 检测新工具并提示
openspec init --tools claude  # 单独为 Claude Code 初始化
openspec update --force  # 强制刷新所有已配置工具的 skills/commands
```

---

## 四大工作流

安装后，Claude Code 中可直接使用以下四种方式与 OpenSpec 交互：

### 🆕 创建变更 — `/opsx:propose` 或 `openspec-propose` skill

```
帮我为「修复涨停列表日期显示问题」创建一个 openspec change
```

或直接使用斜杠命令：

```
/opsx:propose add-stock-export-feature
```

Claude Code 会：
1. 运行 `openspec new change <名称>` 创建目录结构
2. 按依赖顺序生成 `proposal.md` → `specs/` → `design.md` → `tasks.md`
3. 展示最终 status

> **项目中约定**：所有 OpenSpec 产物**默认用中文**编写。如需英文可附在中文之后，但中文必须是主版本。（见 `AGENTS.md` 第 57 条）

### 🔨 实施变更 — `/opsx:apply` 或 `openspec-apply-change` skill

```
帮我执行 upgrade-bilibili-video-visual-quality 这个 change 的任务
```

Claude Code 会：
1. 读取 proposal、design、tasks 获取完整上下文
2. 展示当前进度（已完成/总计任务数）
3. 逐个执行未完成的任务，完成后标记 `[x]`
4. 遇到阻塞时暂停并告知

### 📦 归档变更 — `/opsx:archive` 或 `openspec-archive-change` skill

```
归档 upgrade-bilibili-video-visual-quality 这个 change
```

或使用 CLI：

```bash
# 自动同步 delta specs 到主 specs，跳过确认
openspec archive <变更名> -y

# 跳过 spec 同步（如已在外部手动同步）
openspec archive <变更名> -y --skip-specs
```

归档流程：
1. 检查所有产物和任务是否完成
2. **自动**将 delta specs 同步到 `openspec/specs/`（增量合并）
3. 移动到 `openspec/changes/archive/YYYY-MM-DD-<名称>/`

> **项目中约定**：归档时 Agent **默认自动同步** delta specs，不额外询问确认。（见 `AGENTS.md` 第 56 条）

### 🔍 探索模式 — `/opsx:explore` 或 `openspec-explore` skill

```
帮我研究一下涨停数据流的现状，用 openspec explore 模式
```

Claude Code 会阅读代码、画架构图，但**不写代码**。适合：
- 分析现有代码架构
- 调查问题根因
- 梳理需求
- 方案预研

---

## 实用 CLI 命令速查

| 命令 | 用途 |
|------|------|
| `openspec list` | 列出所有活跃 change |
| `openspec list --specs` | 列出所有能力规格 |
| `openspec view` | 交互式仪表盘 |
| `openspec show <名称>` | 查看某个 change 或 spec 详情 |
| `openspec status --change <名称>` | 查看任务完成状态（含 JSON 输出） |
| `openspec status --change <名称> --json` | JSON 格式状态 |
| `openspec validate <名称>` | 验证 change/spec 格式 |
| `openspec archive <名称> -y` | 归档已完成的 change |
| `openspec archive <名称> -y --skip-specs` | 归档但跳过 spec 同步 |
| `openspec instructions <产物> --change <名称> --json` | 获取生成指定产物的 Agent 指引 |
| `openspec new change <名称>` | 手动创建 change 目录 |
| `openspec config list` | 查看全局配置 |
| `openspec config set delivery both` | 修改 delivery 模式 |
| `openspec init --tools claude` | 为指定工具初始化 skills/commands |
| `openspec update --force` | 强制刷新所有工具的 skills/commands |

---

## Delta Spec 同步机制

每个 Change 下的 `specs/` 目录包含 **Delta Specs**（增量规格），用标记区分变更类型：

```markdown
## ADDED Requirements       # 新增能力
## MODIFIED Requirements    # 修改已有能力
## REMOVED Requirements     # 移除能力
```

归档时，这些 delta specs 会合并到 `openspec/specs/<能力名>/spec.md`（主规格库）中。具体规则：
- **ADDED** → 在主 specs 中创建新能力目录和新 `spec.md`
- **MODIFIED** → 将增量内容精确替换到主 spec 的对应 requirement 中
- **REMOVED** → 从主 spec 中移除对应 requirement

默认工作流下，`openspec archive -y` 会**交互式确认每个 spec 的更新**。如果已手动完成同步，使用 `--skip-specs` 跳过。

---

## 一个完整的使用示例

下面以 StockMaster 项目的 `upgrade-bilibili-video-visual-quality` change 为例，展示完整流程：

### 创建 Change

```
/opsx:propose upgrade-bilibili-video-visual-quality
```

AI 自动生成：
- `proposal.md` — 将 B 站视频从「静态图片循环 + 旁白」升级为分层场景合成
- `design.md` — 技术决策：开源视频工具链、分层合成架构
- `specs/` — 4 个 delta specs（2 个 MODIFIED + 2 个 ADDED）
- `tasks.md` — 15 个实施任务

### 实施任务

```
/opsx:apply upgrade-bilibili-video-visual-quality
```

逐个完成任务，直到 15/15。

### 归档

```
/opsx:archive upgrade-bilibili-video-visual-quality
```

自动执行：
1. 将 `safe-overlay-layout` 和 `scene-visual-spec` 两个 ADDED spec 写入 `openspec/specs/`
2. 将 `wiki-article-video-production` 和 `wiki-article-image-assets` 的 MODIFIED 内容合并进已有主 spec
3. 移动到 `openspec/changes/archive/2026-06-05-upgrade-bilibili-video-visual-quality/`

### 结果

```
openspec list
# → No active changes found.
```

所有历史变更在 `openspec/changes/archive/` 中可追溯。

---

## 项目特有规则（AGENTS.md）

StockMaster 的 `AGENTS.md` 中定义了以下 OpenSpec 相关规则：

1. **归档时自动同步 specs** — Agent 默认必须先把 delta specs 同步到 `openspec/specs/` 再归档，除非用户明确要求跳过同步，否则不单独询问确认。
2. **默认中文编写** — 所有新 OpenSpec 产物默认使用中文。如需英文可附在中文之后，但中文必须是主版本。
3. **真实数据优先** — 不在 spec/proposal/design 中编造虚假数据、文件路径、数量或日期。

---

## 配置迁移：从旧版到新版

如果你的项目之前已有 `.codex/skills/openspec-*/` 或 `.trae/skills/openspec-*/` 的手动配置（非 CLI 生成），运行 `openspec update` 时会自动检测并提示迁移：

```
Detected new tool: Claude Code. Run 'openspec init' to add it.
```

执行 `openspec init --tools claude` 即可为新工具生成标准化的 skills 和 commands。

如果想**统一所有工具的 delivery 模式**：

```bash
# 1. 更新全局 delivery 为 both（同时生成 skills 和 commands）
openspec config set delivery both

# 2. 强制刷新所有已配置工具
openspec update --force
```

---

## 常见问题

### Q: `openspec update` 提示 "No configured tools found"

项目下还没有对应的工具配置目录（如 `.claude/`）。运行 `openspec init --tools claude` 初始化。

### Q: 斜杠命令不生效

重启 IDE。如果仍不生效，确认：
- `.claude/commands/opsx/` 下有对应 `.md` 文件
- `openspec config list` 确认 `delivery` 不是 `skills`（skills-only 模式不会生成 commands）

### Q: 归档时 CLI 卡在交互式确认

使用 `-y` 参数跳过：
```bash
openspec archive <名称> -y
```

### Q: 如何只保留 skills 而不生成 commands

```bash
openspec config set delivery skills
openspec update --force
```

此时 `.claude/commands/opsx/` 会被清理，只保留 `.claude/skills/`。

---

## 相关链接

- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [OpenSpec 官方文档](https://github.com/Fission-AI/OpenSpec/tree/main/docs)
- [StockMaster AGENTS.md](../../../../../../Documents/AbnerPei/Notes/Obsidian/StockMaster/AGENTS.md)
