---
创建日期: 2026-06-03T07:04:35
tags:
  - AI
  - 工具
  - skills
  - GitHub
简介: 收录宝玉维护的多技能仓库，适合按需挑选内容、翻译、配图等工作流。
---

## `baoyu-skills` 是做什么的

这个仓库是宝玉分享的一组 `AI Agent skill` 集合，目标是提升日常工作效率。

根据仓库的 `README`，它包含 `20+` 个 `skill`，并且大体按三类组织：

- 内容类 `skill`
- `AI` 生成类 `skill`
- 实用工具类 `skill`

它覆盖的方向比较广，通常包括：

- 内容生成
- 图片生成
- `Markdown` 转 `HTML`
- 翻译
- 其他实用型工作流

## 它更像“技能集合”，不是单个 `skill`

`baoyu-skills` 更适合被理解成一个 `skill` 仓库，或者一个技能市场集合，而不是单个原子 `skill`。

这意味着使用时最好先确认目标，再决定：

- 是只记录这个仓库
- 还是实际安装它
- 还是只使用其中某个具体 `baoyu-*` 子 `skill`

## 什么时候用

下面这些场景，适合优先想到它：

- 用户给出一个明确的 `GitHub skill` 仓库地址，需要先收录到知识库
- 需要一组现成的 `AI Agent` 工作流，而不是只找单一工具
- 需要处理内容生成、配图、排版、翻译这一类复合任务

## 安装方式

常见安装方式包括：

```bash
npx skills add jimliu/baoyu-skills
```

如果使用支持插件市场的 `Agent`，也可以按仓库说明注册：

```text
/plugin marketplace add JimLiu/baoyu-skills
```

如果后续只想装单个已发布的子 `skill`，仓库说明里也提到了按单项安装的路径，例如：

```bash
clawhub install baoyu-image-gen
```

## 使用时要注意

- 这是一个包含很多 `skill` 的仓库，不建议无脑全量安装
- 更稳妥的做法是先确定具体需求，再选对应的子 `skill`
- 如果只是做资料沉淀，到这里记录仓库信息就够了，不必立即安装

## 我自己的使用备注

以后当我输入类似 `skill:[owner/repo](仓库链接)` 的信息，并明确说明这是 `skill` 时，就按这个目录下的规则新增一篇对应文档。

如果后续这类条目增多，就统一通过 `DB/DB_Skills.base` 来浏览。

## 来源地址

- [`JimLiu/baoyu-skills`](https://github.com/JimLiu/baoyu-skills)
