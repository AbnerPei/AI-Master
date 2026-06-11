---
创建日期: 2026-05-30T22:46:00
title: Pi 的可扩展 Agent Harness
created: 2026-05-30
updated: 2026-05-30
type: concept
tags: [ai, agent, architecture, tooling, workflow]
sources:
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-root-readme.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-agent-core-readme.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-ai-readme.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-extensions.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-skills.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-packages.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-custom-providers.md
confidence: medium
status: evergreen
---

# `Pi` 的可扩展 `Agent Harness`

![](../../raw/A_Assets(素材)/P_Pi/pi-02-agent-stack.png)

## 一句话定义

`Pi` 不是把所有能力直接塞进一个 `AI IDE` 或一个封闭 `CLI`，而是把“模型接入、状态机、工具调用、终端交互、扩展能力”拆成多层，再通过一组稳定接口把这些层重新组合起来。这个可组合底座，就是它所谓的 `agent harness`。

## 三层架构

| 层 | 组件 | 关键职责 |
|---|---|---|
| 模型接入层 | `@earendil-works/pi-ai` | 统一 `provider`、模型发现、`OAuth`、成本与 `context` 序列化 |
| 运行时层 | `@earendil-works/pi-agent-core` | 管理 `agent` 状态、事件流、工具执行、回合推进 |
| 交互层 | `@earendil-works/pi-coding-agent` | 提供终端 `UI`、命令、会话树、项目上下文和扩展加载 |

这种拆分的好处是：你既可以只用底层 `LLM API`，也可以只拿 `agent runtime` 嵌进自己的程序，或者直接把完整 `CLI` 当工作台。

## 为什么叫 `Harness`

这里的 `harness` 不是“再包一层壳”，而是“把不同能力稳定地拴在一起”：

- 模型层负责“和谁说话”。
- 运行时层负责“如何按回合推进，并处理工具调用”。
- 交互层负责“如何让用户、项目文件、命令和扩展进入回路”。

所以 `Pi` 的重点不是某个单一模型或某个单一 `tool`，而是让这些部件能在同一工作流里持续协作。

## 六个主要扩展面

| 机制 | 面向什么问题 | 适合什么时候用 |
|---|---|---|
| `skills` | 给模型补一段按需加载的专门工作流说明 | 某类任务反复出现，但不需要写运行时代码 |
| `extensions` | 给 `Pi` 注入新 `tool`、新命令、事件钩子、自定义 `UI` | 需要真正改变运行时行为 |
| `prompt templates` | 复用固定提示骨架 | 某类任务要稳定复现，但比 `skill` 轻 |
| `themes` | 调整终端表现 | 只改视觉与交互观感 |
| `pi packages` | 把上面这些资源打包分享 | 需要跨项目复用或团队分发 |
| `custom providers` | 代理、企业网关、自托管模型、`OAuth` / `SSO` | 官方内置 `provider` 不够用时 |

这六个面里，最核心的分界线其实是两条：

- `skills` 偏知识和流程。
- `extensions` 偏代码和运行时控制。

`packages` 则是把这些资源变成可安装分发单元。

## `skills` 和 `extensions` 的边界

官方文档对这两个机制的定位很清楚。

`skills` 是“按需加载的能力包”。它更像给模型补一份专门的操作说明、参考材料和脚本入口，本质仍是提示和工作流层。

`extensions` 则是真正的 `TypeScript` 运行时代码。它可以：

- 注册可被模型调用的新 `tool`
- 监听 `session`、`turn`、`tool call` 等事件
- 改写或阻断工具调用
- 增加命令、快捷键、自定义 `UI`
- 注册新的模型 `provider`

所以如果你只是想把 [[LLM Wiki]]、[[OpenSpec 命令与使用详解]] 这种工作流迁进 `Pi`，优先考虑 `skills`。如果你要动 `tool`、`session`、认证或界面行为，就该用 `extensions`。

## 为什么“最小核心”反而重要

`Pi` 的一个显著选择是：它默认不把所有热门 `agent` 功能都塞进核心。官方文档明确提到，像 `sub agents`、`plan mode` 这样的能力，不一定作为内建默认出现，而是交给扩展系统或第三方包。

这带来两个直接结果：

- 核心更容易保持小而稳定。
- 用户可以按自己的工程习惯决定系统最终长什么样。

这和 [[Hermes Agent]] 这类“先提供一整套可运行体验，再围绕体验扩展”的方向并不完全一样。`Pi` 更强调“先有底座，再按工作流拼装”。

## 对当前知识库的启发

对 `AI-Master` 来说，`Pi` 值得长期跟踪的不是某条安装命令，而是它对“`Agent` 产品应该暴露哪些扩展接口”的回答：

- 哪些能力应该做成文档化的 `skill`
- 哪些能力必须进运行时代码
- 如何把 `provider`、`tool`、`session` 和 `UI` 解耦
- 如何让项目规则通过 `AGENTS.md`、`skills`、`extensions` 同时生效

这也是为什么它适合和 [[Pi]]、[[Pi 上手与扩展路线]] 一起看，而不是只看单篇 `README`。

## 相关页面

- [[Pi]]
- [[Pi 上手与扩展路线]]
- [[LLM Wiki]]
- [[Hermes Agent]]
