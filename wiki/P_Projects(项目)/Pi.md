---
创建日期: 2026-05-30T22:46:00
title: Pi
created: 2026-05-30
updated: 2026-05-30
type: project
tags: [ai, agent, tooling, workflow, coding-agent]
sources:
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-root-readme.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-quickstart.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-agent-core-readme.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-ai-readme.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-github-repo-metadata.md
confidence: medium
status: active
---

# `Pi`

![](../../raw/A_Assets(素材)/P_Pi/pi-01-cover.png)

## 定位

`Pi` 是 `earendil-works` 维护的 `AI agent toolkit`。仓库首页把它定义为一个包含自扩展 `coding agent` 的 `agent harness monorepo`，核心由三个包组成：

| 层级 | 包 | 作用 |
|---|---|---|
| 交互层 | `@earendil-works/pi-coding-agent` | 面向终端的交互式 `coding agent CLI` |
| 运行时层 | `@earendil-works/pi-agent-core` | 负责状态、事件流、工具调用和回合推进 |
| 模型接入层 | `@earendil-works/pi-ai` | 统一多家 `LLM provider` 的调用接口、认证和成本统计 |

从 `2026-05-30` 的 `GitHub API` 快照看，仓库默认分支是 `main`，主要语言是 `TypeScript`，项目对外描述已经不只是一个单纯的终端助手，而是一个围绕 `coding agent`、`LLM API`、`TUI`/`Web UI` 组件与配套集成共同演进的工具栈。

## 为什么值得单独整理

`Pi` 的特殊性不在于“再做一个 `CLI`”，而在于它把“可扩展的 `Agent Harness`”当作一等目标：

- 它强调最小核心，不把所有功能都硬编码进主程序。
- 它默认开放 `skills`、`extensions`、`prompt templates`、`themes`、`packages` 和 `custom providers` 这些扩展面。
- 它把 `session`、`branching`、`compaction`、`tool calling`、`OAuth`、`provider handoff` 这些常见 `agent` 基础设施做成可复用底座。
- 它明确接受“你自己继续造能力”，而不是要求用户完全按产品既定路径工作。

这使它更像一个偏工程化的 `agent platform`，而不是只追求开箱即用体验的成品助手。

## 设计取向

`Pi` 官方文档反复强调两点。

第一，它是一个“`minimal terminal coding harness`”。这意味着作者刻意保持核心精简，把很多看起来很“高级”的能力留给扩展系统去实现。

第二，它主张“适配你的工作流，而不是让你适配它”。官方 `README` 甚至直接写明：默认虽然提供强大的基础能力，但像 `sub agents`、`plan mode` 这类功能不一定内建到核心里，而是鼓励你让 `Pi` 自己帮你构建，或者安装第三方 `pi package`。

这个取向和 [[LLM Wiki]] 的思路有相通之处：都更重视“长期可组合、可演化的工作流底座”，而不只是一次性回答。

## 运行形态

围绕 `pi-coding-agent`，官方资料里最稳定的四种使用方式是：

- 交互式终端模式：在当前项目目录直接对话、改文件、跑命令。
- `print` / `json` 模式：做一次性请求或把事件流交给外部程序消费。
- `RPC` 模式：通过标准输入输出接到其他进程或宿主里。
- `SDK` 模式：把 `Pi` 能力嵌入你自己的 `Node.js` 应用。

这使 `Pi` 不只适合“人在终端里驱动模型”，也适合拿来做宿主应用里的 `agent runtime`。

## 供应链与工程纪律

仓库首页还花了不小篇幅讲依赖与发布纪律，这说明它很在意“`agent` 自己会执行代码”带来的供应链风险。当前可见的主要做法包括：

- 安装时推荐使用 `npm install -g --ignore-scripts`。
- 直接外部依赖锁定精确版本。
- 用 `package-lock.json` 和 `npm-shrinkwrap.json` 固定依赖真值。
- 在检查流程里校验锁文件、依赖版本和 `TypeScript` 导入兼容性。
- 用本地发布烟测和定时 `npm audit` 约束发布质量。

对任何想把 `agent` 真正用进日常工程的人来说，这一块比花哨功能更有参考价值。

## 建议阅读顺序

如果后续要继续往这个主题增量整理，建议从下面三页开始：

1. [[Pi 的可扩展 Agent Harness]]：先看它到底把哪些层拆开了。
2. [[Pi 上手与扩展路线]]：再看怎么安装、认证、选择扩展机制。
3. [[AI 资源索引]]：把它放回当前知识库的总导航里看。

## 相关页面

- [[Pi 的可扩展 Agent Harness]]
- [[Pi 上手与扩展路线]]
- [[LLM Wiki]]
- [[AI 资源索引]]
