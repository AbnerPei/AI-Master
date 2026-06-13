---
创建日期: 2026-05-14T16:26:36
tags:
  - AI
  - 工具
  - skills
---

## 这个文件夹是做什么的

这个 `raw/A_Tools(工具)/skills` 文件夹，用来记录我实际在用的 `skill`，以及每个 `skill` 的使用说明。

目标不是只记“这个 `skill` 存在”，而是要记清楚：

- 这个 `skill` 是干什么的。
- 什么场景下应该触发它。
- 它的输入和输出是什么。
- 正确使用顺序是什么。
- 常见坑是什么。

## 当前已整理的 `skill`

- [karpathy-llm-wiki](./karpathy-llm-wiki.md)
- [bilibili-up-info](./bilibili-up-info.md)
- [ai-creator-info](./ai-creator-info.md)
- [channels-video-processor](./channels-video-processor.md)
- [maoxuan-skill](./maoxuan-skill.md)
- [baoyu-skills](./baoyu-skills.md)
- [ian-xiaohei-illustrations](./ian-xiaohei-illustrations.md)
- [cheat-on-content](./cheat-on-content.md)

## 推荐浏览方式

当前 `DB_Skills.base` 默认使用 `List view`，适合做筛选、排序和快速浏览。

如果后面某次 `Obsidian` 版本更新导致 `Base` 视图样式变化，下面这张普通 `Markdown` 导航表可以作为稳定备用入口。

| `Skill` | 简介 |
| --- | --- |
| [baoyu-skills](./baoyu-skills.md) | 收录宝玉维护的多技能仓库，适合按需挑选内容、翻译、配图等工作流。 |
| [maoxuan-skill](./maoxuan-skill.md) | 用《毛选》的矛盾分析和战略框架来拆问题、定优先级和做决策。 |
| [ai-creator-info](./ai-creator-info.md) | 把上游创作者资料生成结构化资料卡，并按分类落盘到知识库。 |
| [bilibili-up-info](./bilibili-up-info.md) | 根据 `B` 站空间链接或 `mid` 获取 `UP` 主基础资料，作为上游查询入口。 |
| [channels-video-processor](./channels-video-processor.md) | 查询微信视频号创作者基础信息，并可继续衔接资料卡生成流程。 |
| [karpathy-llm-wiki](./karpathy-llm-wiki.md) | 用于维护本地 `LLM Wiki` 知识库，支持入库、查询和结构校验。 |
| [ian-xiaohei-illustrations](./ian-xiaohei-illustrations.md) | 用于生成 `Ian` 风格中文正文配图，适合文章、帖子、方法论和工作流类内容的手绘插图生成。 |
| [cheat-on-content](./cheat-on-content.md) | 把内容创作变成 `打分`、`盲预测`、`发布`、`复盘`、`升级 rubric` 的可校准闭环。 |

## `GitHub skill` 收录约定

当我明确给出一个 `GitHub` 地址，并说明“这是 `skill`”时，默认按下面方式沉淀：

- 在 `raw/A_Tools(工具)/skills` 下新增一篇同名 `md`
- 文档名优先使用仓库名，例如 `baoyu-skills.md`
- 在 `frontmatter` 里补一条中文 `简介`，供 `DB_Skills.base` 卡片展示
- 同时把这条 `skill` 追加到本页导航表里
- 文档里至少写清楚：作用、适用场景、安装方式、使用注意点、来源地址
- 如果当前库里还没有对应的 `Base` 数据库，就补建 `DB/DB_Skills.base`

## 后续新增建议

后面每增加一个常用 `skill`，都建议单独新增一篇同名 `md`，至少写清楚下面几项：

- `frontmatter` 里的中文 `简介`
- 作用
- 触发关键词
- 输入
- 输出
- 标准使用流程
- 依赖
- 常见错误
- 我自己的使用备注

## 推荐命名方式

- 文件夹名：保持 `skill` 原名，例如 `bilibili-up-info`
- 文档名：直接使用 `skill` 原名，例如 `bilibili-up-info.md`

这样后面查找、跳转、和源码目录对应都会更直接。
