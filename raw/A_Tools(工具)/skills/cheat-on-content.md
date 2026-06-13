---
创建日期: 2026-06-12T23:42:00
tags:
  - AI
  - 工具
  - skills
  - 内容创作
  - GitHub
简介: 把内容创作变成 `打分`、`盲预测`、`发布`、`复盘`、`升级 rubric` 的可校准闭环。
---

## `cheat-on-content` 是做什么的

`cheat-on-content` 不是普通的“帮你写内容”的 `skill`。

它更像一个给内容创作者用的判断系统，目标是把“我感觉这条会爆”变成可以持续校准的工作流：

- `打分`
- `盲预测`
- `发布`
- `T+3d 复盘`
- `升级 rubric`

它强调的不是多发，而是让自己对内容效果的判断越来越准。

## 它解决的核心问题

很多内容工作流的问题不是不会写，而是：

- 发完内容以后只看结果，不沉淀判断过程
- 下次选题还是凭感觉
- 失败和成功都没有被结构化记录
- 过一段时间后，不知道自己到底学到了什么

`cheat-on-content` 试图解决的就是这个问题。它要求在发布前先把判断写下来，发布后再拿真实数据对账，最后把经验收敛回 `rubric`。

## 它不是单个 `skill`

这个仓库本质上是一个“总路由 `skill` + 一组子 `skill`”：

- 根入口是 `cheat-on-content`
- 下面再拆成多个子流程，例如：
  - `cheat-init`
  - `cheat-learn-from`
  - `cheat-score`
  - `cheat-predict`
  - `cheat-publish`
  - `cheat-retro`
  - `cheat-status`
  - `cheat-bump`

也就是说，它更像一个完整的方法论工具箱，而不是一个只做单点动作的 `skill`。

## 什么时候用

下面这些场景，适合优先想到它：

- 想把自己的内容创作流程做成可复盘的闭环
- 想减少“凭感觉发内容”的成分
- 想建立一套自己的内容评分规则，而不是只听通用建议
- 想持续校准“什么样的内容更适合我的账号”
- 想围绕某个对标账号，反向拆解它的内容规律

如果只是想让 `AI` 直接代写一篇内容，它不是最合适的工具。

## 核心工作流

它的主流程可以理解成 5 步：

1. `初始化`
2. `打分`
3. `盲预测`
4. `发布并记录`
5. `复盘并升级 rubric`

对应到日常使用，大致是这样：

```text
初始化 cheat-on-content
打分这篇 scripts/xxx.md
启动预测 scripts/xxx.md
拍了 / 已发布
复盘 videos/xxx/
状态
升级 rubric
```

## 在 `Codex` 里怎么触发

这个仓库本来兼容 `Claude Code` 和 `Codex`，但在 `Codex` 里不要依赖 `/cheat-*` 这种斜杠命令。

在 `Codex` 里，应该直接用自然语言触发，例如：

- `初始化 cheat-on-content`
- `打分这篇 scripts/foo.md`
- `启动预测 scripts/foo.md`
- `已发布 https://...`
- `复盘 videos/foo/`
- `状态`
- `推荐选题`
- `抓热点`

也就是说，重点不是命令本身，而是让代理路由到对应的子 `skill`。

## 首次使用怎么开始

第一次使用时，必须先跑：

```text
初始化 cheat-on-content
```

初始化阶段会做几件事：

- 判断当前目录是不是一个内容项目目录
- 问你内容形态，例如 `观点视频`、`长文`、`短文`、`播客`
- 问你是否已经发过历史内容
- 问你后续如何拿 `T+3d` 的表现数据
- 询问是否要导入对标账号
- 创建项目脚手架

初始化后，项目目录里通常会出现这些文件和目录：

- `rubric_notes.md`
- `WORKFLOW.md`
- `STATUS.md`
- `.cheat-state.json`
- `scripts/`
- `predictions/`
- `videos/`
- `samples/`
- `candidates.md`

## 这个 `skill` 最重要的三条原则

这是我理解它时必须记住的重点，因为这三条原则决定了它为什么和普通内容工具不一样。

### 1. `Blind prediction`

预测必须在看到真实数据之前写完。

一旦预测写下来了，就不能事后改预测段，只能在后面的复盘段补充真实结果。

这一步的意义是保住“当时你到底怎么判断的”。

### 2. `Bump = full re-score`

如果你想升级 `rubric`，不能只改一条规则就算了。

它要求把校准池里的历史样本按新规则重打一遍，确认新规则确实更贴近真实结果，才能算升级成立。

### 3. `Rubric` 是工作台，不是博物馆

被数据推翻的旧观察，不应该无限堆在文档里。

这个仓库强调把 `rubric` 保持在当前最有效的状态，历史变化交给 `git history` 保存。

## 它特别适合的内容形态

当前内置最明确的是 `观点视频` 类内容，也就是：

- 评论
- 时评
- 论说
- 议题讨论
- 个人观点表达

其他形态也可以用，例如：

- `long-essay`
- `short-text`
- `podcast`
- `tutorial-builder`

只是这些形态通常需要后面自己继续 `bump` 权重，不能完全照搬默认 `rubric`。

## 我这次实际安装时的结论

这次我已经把它安装到本机 `Codex` 的 `skills` 目录里了。

当前稳定源路径是：

- `/Users/peijianbo/.codex/vendor/cheat-on-content`

`Codex` 里的软链接入口在：

- `/Users/peijianbo/.codex/skills/cheat-on-content`
- `/Users/peijianbo/.codex/skills/cheat-init`
- `/Users/peijianbo/.codex/skills/cheat-score`
- `/Users/peijianbo/.codex/skills/cheat-predict`
- 以及其他 `cheat-*` 子 `skill`

这里要注意一个坑：

- 如果把它装在 `/tmp` 下面，再用软链接挂到 `~/.codex/skills`，后面临时目录被系统清掉，这套 `skill` 就会失效
- 更稳妥的方式是像这次一样，把仓库存到稳定目录，再执行 `--codex` 安装

## 安装方式

仓库自带 `install.sh`，可以直接给 `Codex` 安装：

```bash
git clone https://github.com/XBuilderLAB/cheat-on-content.git
cd cheat-on-content
bash install.sh --codex
```

如果想装给 `Claude Code`，则使用默认模式或 `--all`。

安装完成后，通常还需要重启一次 `Codex`，让当前会话识别新增 `skill`。

## 使用时要注意

- 必须先 `初始化`，不要一上来直接 `打分` 或 `预测`
- 在 `Codex` 里用自然语言触发，不要假设 `/cheat-*` 命令一定存在
- 它不是自动代写工具，重点是帮你校准判断
- 没有对标账号也能开始，但早期精度会差很多
- 如果是非 `观点视频` 形态，默认 `rubric` 往往只是起点，后面要自己继续调

## 适合我怎么用

如果后面我要研究某个 `AI` 创作者、拆某类爆款表达，或者自己做内容实验，这个 `skill` 很适合拿来做“内容判断日志”。

我会优先把它理解成：

- 一个内容校准框架
- 一个盲预测日志系统
- 一个围绕 `rubric` 进化的创作工作台

而不是“又一个会帮我写文案的 `AI skill`”。

## 来源地址

- [`XBuilderLAB/cheat-on-content`](https://github.com/XBuilderLAB/cheat-on-content)
- [本地 `SKILL.md`](/Users/peijianbo/.codex/vendor/cheat-on-content/SKILL.md)
- [本地 `cheat-init/SKILL.md`](/Users/peijianbo/.codex/vendor/cheat-on-content/skills/cheat-init/SKILL.md)
