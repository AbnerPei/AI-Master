---
创建日期: 2026-05-19T11:06:36
tags:
  - ai
  - tooling
  - openspec
  - playbook
  - codex
---

# `OpenSpec` 命令与使用详解

这份文档面向“已经知道 `OpenSpec` 是什么，但还没真正把它用顺”的阶段，重点解释三件事：

1. `OpenSpec` 到底在管理什么。
2. `openspec` `CLI` 命令和 `/opsx:*` 聊天命令分别做什么。
3. 在真实项目里，应该按什么顺序使用它，而不是把它变成另一套形式主义文档。

> 说明：
> - 本文命令说明同时参考了官方文档和当前机器上的实测结果。
> - 当前实测环境为 `OpenSpec 1.3.1`、`Node.js 20.20.2`。
> - 本文配图基于你提到的 `image - 2` 作为视觉风格参考生成。

![](../../raw/A_Assets(素材)/O_OpenSpec/openspec-01-cover.png)

## 一、先建立正确理解：`OpenSpec` 不是“多一套文档”，而是“让变更有结构”

很多团队做需求时，真正混乱的不是“不会写代码”，而是下面这条链路断裂了：

- 需求为什么做，没有写清楚。
- 这次改动要影响哪些行为，没有写清楚。
- 技术方案和边界，没有写清楚。
- 实施任务没有拆开，结果 `AI` 或人类工程师只能边猜边改。
- 做完之后，系统当前的“正式行为说明”没有同步，后续又从头猜一遍。

`OpenSpec` 解决的就是这件事。它把一次改动拆成几个稳定的工件：

- `proposal`
- `spec delta`
- `design`
- `tasks`
- `implementation`
- `archive`

你可以把它理解成一个“规范驱动的变更流水线”，而不是一个普通的命令行工具。

![](../../raw/A_Assets(素材)/O_OpenSpec/openspec-02-lifecycle.png)

## 二、`OpenSpec` 管的核心对象是什么

### 1. 主 `specs`

主 `specs` 是系统当前行为的“正式说明书”。

它不是“理想设计稿”，而是“现在这个系统应该如何工作”的源头说明。

例如：

- `auth` 领域现在怎么登录。
- `payments` 领域现在怎么支付。
- `ui` 领域现在怎么切换主题。

### 2. `changes`

`changes` 是每一次拟议中的改动目录。

每个改动会有自己单独的文件夹，例如：

```text
openspec/changes/add-dark-mode/
```

这个目录里通常包含：

- `proposal.md`
- `design.md`
- `tasks.md`
- `specs/` 下的 `delta spec`

### 3. `delta spec`

这是 `OpenSpec` 最关键的概念。

它不是重写整个主规范，而是只描述“这次变更相对于现状新增了什么、修改了什么、删除了什么”。

常见结构是：

- `ADDED Requirements`
- `MODIFIED Requirements`
- `REMOVED Requirements`

归档时，`OpenSpec` 会把这些差量合并回主 `specs`。

![](../../raw/A_Assets(素材)/O_OpenSpec/openspec-03-spec-and-change.png)

## 三、初始化后目录会长什么样

官方推荐在项目里执行：

```bash
openspec init --tools codex /你的项目路径
```

初始化后，典型结构如下：

```text
openspec/
├── specs/
│   └── <domain>/
│       └── spec.md
├── changes/
│   └── <change-name>/
│       ├── proposal.md
│       ├── design.md
│       ├── tasks.md
│       └── specs/
│           └── <domain>/
│               └── spec.md
└── config.yaml
```

如果你给 `Codex` 开启了工具适配，还会生成：

```text
.codex/skills/openspec-propose/SKILL.md
.codex/skills/openspec-explore/SKILL.md
.codex/skills/openspec-apply-change/SKILL.md
.codex/skills/openspec-archive-change/SKILL.md
```

这意味着：终端里的 `openspec` 负责“项目结构和状态管理”，聊天里的 `/opsx:*` 负责“让 `AI` 按这套结构做事”。

![](../../raw/A_Assets(素材)/O_OpenSpec/openspec-05-project-structure.png)

## 四、最容易混淆的一点：它其实有两套命令系统

### 1. 终端里的 `CLI`

也就是：

```bash
openspec init
openspec list
openspec validate
```

这一层的职责是：

- 初始化项目
- 更新工具配置
- 查看 `spec` / `change`
- 校验结构
- 归档变更
- 管理 `schema` / `config`

### 2. 聊天里的 `/opsx:*`

也就是：

```text
/opsx:propose
/opsx:apply
/opsx:archive
```

这一层的职责是：

- 让 `AI` 创建变更工件
- 让 `AI` 按任务实施
- 让 `AI` 归档和同步

一句话总结：

- `CLI` 是管理层。
- `/opsx:*` 是执行层。

![](../../raw/A_Assets(素材)/O_OpenSpec/openspec-04-command-groups.png)

## 五、`CLI` 命令详解

下面按“你在真实项目里最常用的顺序”来讲。

### 1. `openspec init`

作用：初始化 `OpenSpec` 项目结构，并生成对应 `AI` 工具的接入文件。

命令：

```bash
openspec init [path]
```

常用参数：

- `--tools <list>`：指定要给哪些 `AI` 工具生成接入文件。
- `--force`：清理旧文件并强制初始化。
- `--profile <profile>`：指定本次初始化使用的配置档。

最常用示例：

```bash
openspec init --tools codex .
openspec init --tools claude,cursor ./my-project
openspec init --tools all
```

什么时候用：

- 你第一次给一个代码仓库接入 `OpenSpec`。
- 你新建了一个项目，准备从一开始就按规范驱动开发。

注意点：

- 这一步只需要做一次。
- 做完通常需要重启 `IDE` 或刷新工具环境，让新生成的命令生效。

### 2. `openspec update`

作用：升级或刷新 `OpenSpec` 生成的工具接入文件。

命令：

```bash
openspec update [path]
```

常用参数：

- `--force`

什么时候用：

- 你升级了 `OpenSpec`。
- 你改了 `profile`。
- 你改了全局 `workflow` 选择。
- 你发现本地接入文件还是旧的。

常用示例：

```bash
openspec update
openspec update --force
```

### 3. `openspec list`

作用：列出当前的 `change` 或 `spec`。

命令：

```bash
openspec list
openspec list --specs
```

常用参数：

- `--specs`
- `--changes`
- `--sort recent|name`
- `--json`

什么时候用：

- 想看当前有哪些活跃变更。
- 想看主 `spec` 里有哪些领域。
- 想让脚本或 `AI` 以结构化方式消费结果。

### 4. `openspec show`

作用：查看某个 `change` 或 `spec` 的具体内容。

命令：

```bash
openspec show <item-name>
```

常用参数：

- `--json`
- `--type change|spec`
- `--deltas-only`
- `--requirements`
- `--no-scenarios`
- `-r, --requirement <id>`

什么时候用：

- 想直接看某个变更的细节。
- 想只看 `delta spec`。
- 想让 `AI` 精确读取某个需求。

示例：

```bash
openspec show add-dark-mode
openspec show auth --type spec
openspec show add-dark-mode --json --deltas-only
```

### 5. `openspec view`

作用：以交互式面板查看 `spec` 和 `change`。

命令：

```bash
openspec view
```

什么时候用：

- 你想更直观看当前项目里有哪些变更和规范。

注意点：

- 它更偏人类交互，不适合脚本化。

### 6. `openspec validate`

作用：校验 `spec` 和 `change` 的结构与内容是否符合规范。

命令：

```bash
openspec validate [item-name]
```

常用参数：

- `--all`
- `--changes`
- `--specs`
- `--type change|spec`
- `--strict`
- `--json`
- `--no-interactive`

什么时候用：

- 规划工件写完以后。
- 归档之前。
- 你怀疑某个 `delta spec` 写得不规范时。
- 你想在自动化里做批量校验时。

示例：

```bash
openspec validate add-dark-mode
openspec validate --all
openspec validate --all --strict --json
```

### 7. `openspec status`

作用：查看某个 `change` 的工件完成状态。

命令：

```bash
openspec status --change <id>
```

常用参数：

- `--change <id>`
- `--schema <name>`
- `--json`

什么时候用：

- 你不知道当前变更已经做到哪一步。
- 你不确定缺的是 `proposal`、`design` 还是 `tasks`。
- 你需要给 `AI` 一个结构化的当前状态视图。

### 8. `openspec instructions`

作用：输出针对某个工件或某个变更的增强执行指令。

命令：

```bash
openspec instructions
openspec instructions --change <id>
```

常用参数：

- `--change <id>`
- `--schema <name>`
- `--json`

什么时候用：

- 你想把“下一步该怎么做”交给另一个 `AI` 代理。
- 你需要明确当前工件的撰写规范。

### 9. `openspec archive`

作用：归档完成的变更，并把 `delta spec` 合并回主 `spec`。

命令：

```bash
openspec archive <change-name>
```

常用参数：

- `-y, --yes`
- `--skip-specs`
- `--no-validate`

什么时候用：

- 任务已经实施完成。
- 你确认这次变更应该进入系统正式规范。

示例：

```bash
openspec archive add-dark-mode
openspec archive add-dark-mode -y
```

注意点：

- `--skip-specs` 适合纯工具链、纯文档、纯流程类变更。
- `--no-validate` 不建议常用，除非你非常确定只是为了紧急收尾。

### 10. `openspec config`

作用：管理全局配置。

命令：

```bash
openspec config list
openspec config get <key>
openspec config set <key> <value>
openspec config unset <key>
openspec config profile
```

最值得关注的是：

```bash
openspec config profile
```

因为它决定了你启用哪套工作流。

官方默认 `core` 通常包含：

- `propose`
- `explore`
- `apply`
- `sync`
- `archive`

但当前机器实测到的全局配置是：

```text
profile: custom
delivery: skills
workflows: propose, explore, apply, archive
```

这意味着本机目前没有显式启用 `sync`、`new`、`continue`、`ff`、`verify` 这些工作流，需要通过：

```bash
openspec config profile
openspec update
```

重新选择并刷新。

### 11. `openspec new`

作用：创建一个新的 `change` 骨架。

命令：

```bash
openspec new change <name>
```

什么时候用：

- 你不想一步到位生成全部规划工件。
- 你想先建目录，再逐步补 `proposal`、`spec`、`design`、`tasks`。

这和 `/opsx:new` 的理念一致，只不过这是 `CLI` 入口。

### 12. `openspec change` 与 `openspec spec`

作用：分别管理 `change` 和主 `spec`。

命令示例：

```bash
openspec change show add-dark-mode
openspec change validate add-dark-mode
openspec spec list
openspec spec show auth
```

理解方式：

- 它们更多是“分类入口”。
- 日常使用上，官方已经更推荐顶层的 `list`、`show`、`validate`。

### 13. `openspec schemas` / `schema` / `templates`

这是进阶区。

#### `openspec schemas`

作用：列出当前可用的工作流 `schema`。

示例：

```bash
openspec schemas
openspec schemas --json
```

当前机器实测只看到一个内置 `schema`：

- `spec-driven`

#### `openspec templates`

作用：查看当前 `schema` 各工件使用的模板路径。

示例：

```bash
openspec templates
openspec templates --json
```

当前实测模板包括：

- `proposal`
- `specs`
- `design`
- `tasks`

#### `openspec schema`

作用：创建、复制、校验自定义 `schema`。

可用子命令：

- `schema init`
- `schema fork`
- `schema validate`
- `schema which`

什么时候用：

- 团队要自定义工件结构。
- 你觉得默认 `spec-driven` 不适合自己的研发方式。
- 你要增加特定模板，例如评审模板、风险模板、迁移模板。

### 14. `openspec completion`

作用：安装或生成 `shell` 自动补全。

示例：

```bash
openspec completion generate zsh
openspec completion install zsh
```

### 15. `openspec feedback`

作用：向官方提交反馈。

### 16. `openspec workspace`

这里要特别说明。

官方最新 `CLI` 文档里已经出现了 `workspace` 这组命令，而且标记为 `beta`，包括：

- `workspace setup`
- `workspace list`
- `workspace link`
- `workspace relink`
- `workspace doctor`
- `workspace update`
- `workspace open`

但当前机器实测的 `OpenSpec 1.3.1` 顶层帮助里还没有展示 `workspace` 命令。

这说明两件事：

1. 官方文档更新速度可能领先于你当前安装版本。
2. 遇到这种情况，优先以本机 `openspec --help` 为准，再决定是否升级。

结论：

- 如果你只是在单仓库里使用 `OpenSpec`，先忽略 `workspace`。
- 如果你未来要做多仓库规划，再单独研究这组 `beta` 命令。

## 六、`/opsx:*` 聊天命令详解

如果说 `CLI` 是管理层，那么 `/opsx:*` 就是你平时和 `AI` 协作时最常用的部分。

### 1. 默认快速路径

官方的默认快速路径是：

```text
/opsx:propose -> /opsx:apply -> /opsx:sync -> /opsx:archive
```

它的意思是：

1. 先创建并补齐规划工件。
2. 再实施代码修改。
3. 再把 `delta spec` 同步回主 `spec`。
4. 最后归档。

### 2. 扩展路径

如果你启用了扩展工作流，官方还支持：

```text
/opsx:new -> /opsx:ff 或 /opsx:continue -> /opsx:apply -> /opsx:verify -> /opsx:archive
```

这更适合复杂项目或想逐步审阅的人。

![](../../raw/A_Assets(素材)/O_OpenSpec/openspec-06-planning-stage.png)

### 3. `/opsx:propose`

作用：一步创建一个 `change`，并自动生成规划工件。

命令示例：

```text
/opsx:propose add-dark-mode
/opsx:propose 为移动端增加 JWT 登录
```

它通常会生成：

- `proposal.md`
- `spec delta`
- `design.md`
- `tasks.md`

适合什么时候用：

- 你想走最快路径。
- 需求已经比较明确。

### 4. `/opsx:explore`

作用：先探索，不立即创建正式变更。

命令示例：

```text
/opsx:explore
/opsx:explore 我们现有的鉴权方式是否适合移动端
```

适合什么时候用：

- 需求还不清楚。
- 你需要先调查代码现状。
- 你要比较多种方案。

特点：

- 这个阶段不强制生成工件。
- 更像“调研 + 方案收敛”。

### 5. `/opsx:new`

作用：先创建变更骨架，不一次生成所有规划工件。

适合什么时候用：

- 你想严格控制每一步。
- 需求大、边界多、风险高。

### 6. `/opsx:continue`

作用：基于依赖关系，生成下一个应该出现的工件。

适合什么时候用：

- 你想一步一步推进。
- 你希望先审完上一个工件，再生成下一个。

### 7. `/opsx:ff`

这里的 `ff` 是 `fast-forward`。

作用：把规划阶段一次性补齐。

适合什么时候用：

- 需求清晰。
- 项目规模适中。
- 你不想每个工件都手动过一遍。

### 8. `/opsx:apply`

作用：按 `tasks.md` 实施改动。

它通常会：

- 读取 `tasks`
- 逐项执行
- 修改代码
- 运行必要验证
- 勾选完成项

![](../../raw/A_Assets(素材)/O_OpenSpec/openspec-07-implementation-and-validation.png)

### 9. `/opsx:verify`

作用：验证“实现结果是否符合前面工件的描述”。

适合什么时候用：

- 需求复杂。
- 你担心实现偏离 `spec` 或 `design`。
- 你想在归档前多一道一致性检查。

### 10. `/opsx:sync`

作用：把 `delta spec` 同步到主 `spec`。

注意：

- 官方默认快速路径里有它。
- 但当前机器的全局 `workflow` 没有显式启用它。

如果你需要它，应先重新配置 `profile` 并执行：

```bash
openspec config profile
openspec update
```

### 11. `/opsx:archive`

作用：归档已经完成的变更。

这个阶段通常意味着：

- 规划完成
- 实现完成
- 规范同步完成
- 变更目录进入归档区

### 12. 其他扩展命令

官方文档还提到：

- `/opsx:bulk-archive`
- `/opsx:onboard`

这类命令更偏团队批量处理或新手引导，不是日常主线。

## 七、推荐你怎么用：四种最实用打法

### 1. 最快路径：适合大多数普通功能

步骤：

```text
/opsx:propose
/opsx:apply
/opsx:sync
/opsx:archive
```

适合：

- 新功能
- 小到中等复杂度改动
- 需求已经明确

### 2. 稳一点的路径：适合需求还没定型

步骤：

```text
/opsx:explore
/opsx:propose
/opsx:apply
/opsx:archive
```

适合：

- 历史代码复杂
- 需要先调研
- 需求边界模糊

### 3. 严格控制路径：适合大改动

步骤：

```text
/opsx:new
/opsx:continue
/opsx:continue
/opsx:continue
/opsx:apply
/opsx:verify
/opsx:archive
```

适合：

- 架构改造
- 跨模块重构
- 涉及多人协作

### 4. 纯工具链或纯文档类变更

如果这次变更不真的改变产品行为，而只是：

- 增加脚本
- 更新流程
- 补文档
- 改工具接入

那么归档时可以考虑：

```bash
openspec archive <change-name> --skip-specs
```

这样不会强行把无关内容塞进主行为规范里。

![](../../raw/A_Assets(素材)/O_OpenSpec/openspec-08-openspec-vs-ad-hoc.png)

## 八、一个完整示例：从零开始推进一个变更

假设你要做“增加深色模式”。

### 1. 初始化

```bash
openspec init --tools codex .
```

### 2. 创建变更

```text
/opsx:propose add-dark-mode
```

此时通常会生成：

- `proposal.md`
- `specs/ui/spec.md`
- `design.md`
- `tasks.md`

### 3. 开始实施

```text
/opsx:apply
```

### 4. 用 `CLI` 校验状态

```bash
openspec list
openspec show add-dark-mode
openspec validate add-dark-mode
openspec status --change add-dark-mode
```

### 5. 完成后归档

```text
/opsx:archive
```

或者终端里：

```bash
openspec archive add-dark-mode
```

## 九、常见误区与规避方式

### 误区 1：只装了 `OpenSpec`，但没跑 `init`

结果：

- 聊天命令不可用。
- 项目里没有 `openspec/` 目录。

规避方式：

```bash
openspec init --tools codex .
```

### 误区 2：把 `CLI` 命令和 `/opsx:*` 当成一回事

结果：

- 不知道为什么终端里没有 `/opsx:propose`。
- 不知道为什么聊天里不能直接执行 `openspec list`。

规避方式：

- 记住：前者是终端管理层，后者是聊天执行层。

### 误区 3：改了 `profile`，但没执行 `update`

结果：

- 新工作流没有同步到项目接入文件。

规避方式：

```bash
openspec config profile
openspec update
```

### 误区 4：把每一次小改动都做成超大 `change`

结果：

- `proposal` 写不清。
- `tasks` 过大。
- `AI` 实施时容易飘。

规避方式：

- 一个 `change` 只做一个清晰目标。
- 变更要小而闭合。

### 误区 5：实施完成了，但主 `spec` 没同步

结果：

- 下一轮改动又要重新猜系统行为。

规避方式：

- 明确把 `sync` / `archive` 当成闭环的一部分，而不是可有可无。

### 误区 6：看到官方文档有命令，本机却没有

结果：

- 以为自己装坏了。

实际原因通常是：

- 你本机版本较旧。
- 官方文档已经更新到更高版本能力。

规避方式：

- 先看本机：

```bash
openspec --help
openspec --version
```

- 再决定是否升级。

![](../../raw/A_Assets(素材)/O_OpenSpec/openspec-09-best-practices.png)

## 十、我对 `OpenSpec` 的实用建议

如果你要把 `OpenSpec` 真正用起来，不要追求“每个命令都懂”，先做到下面四点：

1. 先分清 `CLI` 和 `/opsx:*`。
2. 先跑通一条最短闭环：`propose -> apply -> archive`。
3. 每次只做一个清晰的 `change`。
4. 把归档当成正式完成，而不是把代码改完就算结束。

对多数个人开发者或小团队来说，真正高频的是这些：

- `openspec init`
- `openspec update`
- `openspec list`
- `openspec show`
- `openspec validate`
- `openspec archive`
- `/opsx:propose`
- `/opsx:explore`
- `/opsx:apply`
- `/opsx:archive`

只要先把这 10 个动作用顺，`OpenSpec` 的价值就已经出来了。

## 十一、官方参考链接

- [官方仓库](https://github.com/Fission-AI/OpenSpec)
- [官方 `Getting Started`](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md)
- [官方 `Commands`](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
- [官方 `CLI`](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)
- [官方 `Supported Tools`](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)

## 十二、配图清单

本文使用的配图文件如下，均位于：

```text
raw/A_Assets(素材)/O_OpenSpec/
```

- `openspec-01-cover.png`
- `openspec-02-lifecycle.png`
- `openspec-03-spec-and-change.png`
- `openspec-04-command-groups.png`
- `openspec-05-project-structure.png`
- `openspec-06-planning-stage.png`
- `openspec-07-implementation-and-validation.png`
- `openspec-08-openspec-vs-ad-hoc.png`
- `openspec-09-best-practices.png`
