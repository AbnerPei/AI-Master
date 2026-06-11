---
创建日期: 2026-05-17T20:26:47
tags:
  - ai
  - tooling
  - openspec
  - playbook
---

# `OpenSpec` 安装与使用

这份文档记录 `OpenSpec` 在当前机器上的实际安装结果、踩坑点，以及后续在 `Codex` 里可直接复用的初始化方式。

## `OpenSpec` 是什么

`OpenSpec` 是一个面向 `AI-native` 开发流程的规范驱动工具。它会在项目里生成 `spec`、`change`、指令和配套 `AI` 工具适配层，用来把“提需求、拆变更、落规范、校验状态”这条链路结构化。

官方入口：

- [`OpenSpec` 官方仓库](https://github.com/Fission-AI/OpenSpec)
- [`OpenSpec` `npm` 包](https://www.npmjs.com/package/@fission-ai/openspec)

## 当前机器安装结果

- 已安装 `OpenSpec` 版本：`1.3.1`
- 命令路径：`/Users/peijianbo/.local/share/mise/shims/openspec`
- 实际生效 `Node.js` 版本：`v20.20.2`
- `npm` 版本：`10.8.2`

可直接验证：

```bash
openspec --version
```

## 这次安装里遇到的关键问题

`OpenSpec` 官方要求 `Node.js >=20.19.0`，而这台机器原先默认命中的其实是 `DevEco Studio` 自带的旧版 `node`，版本只有 `v18.20.1`，直接安装会卡在运行时要求上。

这次的处理方式是：

```bash
mise use -g node@20
npm install -g @fission-ai/openspec
```

为了让新开的 `zsh` 终端默认优先使用 `mise` 管理的 `Node.js`，还额外处理了 `~/.zshrc`：

- 启用 `mise activate`
- 把 `~/.local/share/mise/shims` 放到最终 `PATH` 前面

如果以后又发现 `node --version` 退回到旧版本，优先检查是不是别的工具链把自己的 `node` 抢到了 `PATH` 前面。

## 常用命令

`OpenSpec` 安装完成后，当前可直接使用这些命令：

```bash
openspec --help
openspec init --help
openspec list
openspec show <item-name>
openspec validate
openspec archive <change-name>
openspec instructions --change <change-id>
openspec config list
```

它们的大致用途：

- `openspec init`：给项目初始化 `OpenSpec` 目录和目标 `AI` 工具适配文件。
- `openspec list`：查看当前 `change` 或 `spec` 列表。
- `openspec show`：看某个 `change` 或 `spec` 的详情。
- `openspec validate`：校验规范与变更结构是否完整。
- `openspec archive`：归档已完成的变更。
- `openspec instructions`：输出面向 `AI` 执行的增强指令。

## 在 `Codex` 里初始化一个项目

如果后面要给某个项目接入 `OpenSpec`，推荐直接执行：

```bash
openspec init --tools codex /你的项目路径
```

`OpenSpec 1.3.1` 的 `init` 支持通过 `--tools` 指定目标 `AI` 工具，当前 `Codex` 已在官方支持列表里。

这次我在临时目录做了实际验证：

```bash
openspec init --tools codex /tmp/openspec-demo.xxxxxx
```

初始化完成后，核心结构如下：

```text
.codex/skills/openspec-propose/SKILL.md
.codex/skills/openspec-explore/SKILL.md
.codex/skills/openspec-apply-change/SKILL.md
.codex/skills/openspec-archive-change/SKILL.md
openspec/changes/
openspec/specs/
```

命令行还会提示：

- 以后可以从 `/opsx:propose "your idea"` 开始第一条变更
- 需要重启 `IDE`，新的斜杠命令才会生效

## 当前建议

这次只完成了“全局安装 + 验证”，没有在 `AI-Master` 仓库里直接执行 `openspec init`。这样做的原因很简单：这个仓库本质上是知识库，不是典型的软件工程仓库，先保留手动初始化权更稳妥。

如果后面你希望我把 `OpenSpec` 真的接到某个代码仓库里，建议直接告诉我目标仓库路径，我就可以继续把：

- `openspec init`
- 首个 `change proposal`
- 与当前 `Codex` 工作流的结合方式

一起落完整。

## 可选项

如果不想让 `OpenSpec` 上报匿名统计，可以在 `shell` 环境里加：

```bash
export OPENSPEC_TELEMETRY=0
```
