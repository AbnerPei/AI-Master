---
创建日期: 2026-05-30T22:46:00
title: Pi 上手与扩展路线
created: 2026-05-30
updated: 2026-05-30
type: playbook
tags: [ai, agent, tooling, workflow, playbook]
sources:
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-quickstart.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-extensions.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-skills.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-packages.md
  - ../../raw/A_AI-Agent-Tech-Stack/P_Pi/2026-05-30-pi-custom-providers.md
confidence: medium
status: evergreen
---

# `Pi` 上手与扩展路线

![](../../raw/A_Assets(素材)/P_Pi/pi-03-extensibility-map.png)

## 适用场景

这页适合两类人：

- 想快速跑通一次 `Pi` 的安装、认证和首次会话。
- 已经知道自己要做 `AI` 工作流，但还不清楚该把能力放进 `AGENTS.md`、`skills`、`extensions` 还是 `packages`。

## 第一步：先装起来

官方推荐安装命令是：

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

这里的关键不是“会不会装”，而是它明确把 `--ignore-scripts` 当默认建议，说明项目非常在意依赖生命周期脚本带来的供应链风险。

卸载时，根据安装方式使用对应包管理器；如果是 `npm` 或官方 `curl` 安装路径，本质上都回到：

```bash
npm uninstall -g @earendil-works/pi-coding-agent
```

卸载不会清掉 `~/.pi/agent/` 下的设置、认证、会话和已安装 `pi packages`。

## 第二步：选认证方式

`Pi` 支持两条主路。

### 订阅登录

启动后直接在交互界面里执行：

```text
/login
```

官方文档里明确提到的内置订阅登录包括：

- `Claude Pro/Max`
- `ChatGPT Plus/Pro (Codex)`
- `GitHub Copilot`

### `API key`

如果你走密钥路径，最直接的是先设环境变量，再启动：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
pi
```

## 第三步：做一次有效的首会话

官方 `quickstart` 给的思路非常朴素：先在你真正想工作的项目目录里启动 `Pi`，再让它对当前仓库做一件小而完整的事情。

例如：

```text
Summarize this repository and tell me how to run its checks.
```

默认情况下，模型会拿到四个基础 `tool`：

- `read`
- `write`
- `edit`
- `bash`

也就是说，第一次会话最好不要问空泛问题，而是让它围绕一个具体项目做一次“读文件 + 改文件 + 跑命令”的闭环。

## 第四步：先把项目规则写进 `AGENTS.md`

`Pi` 会在启动时加载上下文文件。官方文档列出的优先路径包括：

- `~/.pi/agent/AGENTS.md`
- 当前目录和父目录里的 `AGENTS.md` 或 `CLAUDE.md`

因此，对项目级约束、测试要求、禁区路径、回答风格，优先写进 `AGENTS.md`。这一步的收益远高于一开始就写复杂扩展。

对当前 `AI-Master` 仓库来说，这一点尤其重要，因为这里已经有明确的 `Markdown` 规范和 `Obsidian` 写作约束。把这些规则稳定前置，比让模型每次临时猜测更可靠。

## 第五步：怎么选扩展机制

| 机制 | 用来解决什么问题 | 什么时候选它 |
|---|---|---|
| `AGENTS.md` | 项目级行为约束、输出格式、禁区规则 | 任何项目都应该先配这个 |
| `skills` | 复用某类任务的操作说明、参考资料、脚本入口 | 像 [[LLM Wiki]] 这类可复用工作流 |
| `extensions` | 新 `tool`、命令、钩子、`UI`、会话行为、`provider` | 需要真代码介入运行时 |
| `custom providers` | 公司代理、自托管模型、企业 `OAuth`、非标准 `API` | 默认 `provider` 不够用时 |
| `pi packages` | 分发 `skills`、`extensions`、`themes`、提示模板 | 需要跨项目或团队共享时 |

一个简单判断法：

- 如果你主要在补“知识和流程”，先做 `skill`。
- 如果你主要在改“系统行为”，先做 `extension`。
- 如果你已经做出来并想复用或分享，再打成 `pi package`。

## 对当前仓库的落地建议

如果要把 `Pi` 真正接进 `AI-Master` 这类知识库工程，建议路线是：

1. 继续把当前的仓库规范放在 `AGENTS.md`。
2. 把 `karpathy-llm-wiki` 这类稳定流程继续沉淀成 `skill`。
3. 只有在需要额外 `tool`、目录扫描器、素材处理器、`provider` 代理时，再补 `extension`。
4. 当这些能力跨仓库复用时，再考虑打成 `pi package`。

这条路线的优点是：不会一上来就把所有事情都工程化，同时又给后续真正的运行时扩展留足空间。

## 下一步阅读

- [[Pi]]
- [[Pi 的可扩展 Agent Harness]]
- [[LLM Wiki]]
- [[OpenSpec 命令与使用详解]]
