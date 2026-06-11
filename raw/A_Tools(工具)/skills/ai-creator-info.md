---
创建日期: 2026-05-14T16:26:36
tags:
  - AI
  - 工具
  - skills
  - 创作者
简介: 把上游创作者资料生成结构化资料卡，并按分类落盘到知识库。
---

## `ai-creator-info` 是做什么的

这个 `skill` 用来把上游已经查询到的创作者 `JSON`，加工成 `Obsidian` 风格的资料 `md` 文档。

它不是平台查询器，而是资料生成器。

## 正确职责

它做的是：

- 接收上游 `JSON`
- 询问分类
- 询问星级
- 生成最终 `md`
- 保存到 `raw/` 的对应分类目录

它不做的是：

- 不直接抓平台数据
- 不重复联网查询

## 什么时候用

当我的目标是下面这些事情时，就应该想到这个 `skill`：

- 记录某个 `AI` 创作者
- 收藏某个 `AI` 大神
- 生成创作者资料卡
- 落盘到 `AI-Master/raw`

## 正确使用顺序

标准顺序是：

1. 先用上游查询 `skill` 拿到 `JSON`
2. 让用户确认分类
3. 让用户确认星级
4. 再用 `ai-creator-info` 生成 `md`

上游一般可能是：

- `bilibili-up-info`
- `channels-video-processor`

## 分类和星级

常见分类：

1. `AI 大神`
2. `AI 创作者`
3. 两者都是

星级：

- `1` 到 `5`

这个 `skill` 的关键点之一，是生成前必须拿到明确的分类和星级，不要静默默认。

## 常见命令形态

```bash
python3 {skill_path}/scripts/generate_profile.py \
  --json '{JSON字符串}' \
  --category "AI 创作者" \
  --stars 4
```

也可以传 `--json-file`。

## 产出结果

最终会生成结构化的 `md` 文档，并按分类放到 `raw/` 目录下。

在当前这套工作流里，如果存在：

- `/Users/peijianbo/Documents/MeMe/AI-Master/raw`

就优先写到这个资料库里。

## 我自己的使用备注

这个 `skill` 是“资料落盘器”。只要已经拿到上游 `JSON`，就应该直接复用，不要再次发起查询。

## 源路径

- `/Users/peijianbo/.agents/skills/ai-creator-info/SKILL.md`
