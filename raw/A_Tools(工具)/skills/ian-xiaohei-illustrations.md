---
创建日期: 2026-06-06T22:56:47
tags:
  - AI
  - 工具
  - skills
  - GitHub
  - 配图
简介: 用于生成 `Ian` 风格中文正文配图，适合文章、帖子、方法论和工作流类内容的手绘插图生成。
---

## `ian-xiaohei-illustrations` 是做什么的

这个 `skill` 用来给中文文章生成 `Ian` 风格的正文配图。

它不是常规商业插画，也不是 `PPT` 信息图，而是偏：

- 纯白背景
- 黑色手绘线稿
- 少量红橙蓝中文批注
- 大量留白
- “小黑”作为核心动作主体

它最适合把一段正文里的核心判断、流程、结构、状态或隐喻，转成一张 `16:9` 的横版手绘解释图。

## 什么时候用

下面这些场景，适合优先想到它：

- 需要给中文长文、帖子、博客、`Notion` 文档补正文配图
- 需要先分析一篇文章哪些段落值得配图
- 需要输出一组 `shot list`
- 需要基于同一篇正文批量生成多张统一风格插图
- 需要对已有图做“去标题”“改图”“增强怪诞感”这一类迭代

如果目标只是做普通封面图、课程图解、正式流程图、商业插画，这个 `skill` 就不太合适。

## 它的核心工作方式

这个 `skill` 的工作流比较明确：

1. 先读正文，提炼真正值得配图的认知锚点
2. 如果用户还没要求直接出图，就先给 `shot list`
3. 每张图只讲一个核心结构，不把多张图拼在一起
4. 生成后按检查清单看是否太满、太像 `PPT`、太可爱，或者“小黑”只是装饰
5. 如果在 `workspace` 内工作，再把最终图片按顺序落到 `assets/<article-slug>-illustrations/`

## 触发关键词

这个 `skill` 的触发词比较集中，常见包括：

- `正文配图`
- `文章插图`
- `配图建议`
- `shot list`
- `去标题`
- `改图`
- `怪诞`
- `小黑`
- `手绘`

## 安装方式

如果只是做资料收录，到这里记录仓库信息就够了。

如果要真正装到本地 `Codex skills`，可以使用之前的安装脚本：

```bash
python3 /Users/peijianbo/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo helloianneo/ian-xiaohei-illustrations --path ian-xiaohei-illustrations
```

当前机器上我已经装过一份，路径是：

- `/Users/peijianbo/.codex/skills/ian-xiaohei-illustrations`

## 使用时要注意

- 默认目标是中文正文配图，不是泛用图片生成
- 先判断正文哪些段落值得配图，不要平均分配
- 默认视觉主体必须是“小黑”，而且它要参与核心动作
- 不要做成 `PPT`、课件、正式架构图或儿童插画
- 颜色要克制，重点是黑色线稿加少量红橙蓝批注
- 每张图只讲一个意思，宁可拆成多张，也不要一张图塞太多信息

## 我自己的使用备注

这个 `skill` 很适合和“先整理内容结构，再决定哪些段落配图”的写作流程一起用。

如果后面我在 `AI-Master` 里整理文章工作流、方法论文档、产品说明或者知识卡片，需要一套统一但不死板的正文插图风格，这个 `skill` 的匹配度会比较高。

## 来源地址

- [`helloianneo/ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations)

## 源路径

- `/Users/peijianbo/.codex/skills/ian-xiaohei-illustrations/SKILL.md`
