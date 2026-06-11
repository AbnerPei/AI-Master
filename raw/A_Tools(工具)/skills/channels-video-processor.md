---
创建日期: 2026-05-14T16:26:36
tags:
  - AI
  - 工具
  - skills
  - 视频号
简介: 查询微信视频号创作者基础信息，并可继续衔接资料卡生成流程。
---

## `channels-video-processor` 是做什么的

这个 `skill` 用来处理微信视频号创作者资料。

它的职责边界和 `bilibili-up-info` 很接近，但平台换成了视频号。

它主要做两件事：

- 查询视频号创作者基础信息
- 在需要时继续调用 `ai-creator-info` 生成资料 `md`

## 什么时候用

当输入里出现下面这些内容时，优先想到这个 `skill`：

- 视频号
- 微信视频号
- `finder ID`
- `channels.weixin.qq.com`
- `weixin.qq.com/sph/...`

## 特别规则

只要链接域名是 `weixin.qq.com`，并且路径里带 `/sph/`，就按微信视频号短链处理。

这是这个 `skill` 里一个非常关键的判断规则。

## 常见输入

- 视频号主页链接
- 视频号短链
- `finder ID`

例如：

- `https://channels.weixin.qq.com/finder-preview/pages/sph?id=ANFZXzn3N9`
- `https://weixin.qq.com/sph/Av0dEnlvVz`

## 两种典型用法

### 只查基础资料

如果我只是想看创作者信息，到查询 `JSON` 就可以结束。

### 查询后直接生成 `md`

如果当前语境是整理 `AI` 创作者资料，就不要停在 `JSON`，而是继续：

1. 展示查询结果
2. 确认分类
3. 确认星级
4. 调用 `ai-creator-info` 落盘

## 常见命令形态

只查资料：

```bash
python3 {skill_path}/scripts/fetch_channels_info.py "<视频号URL>"
```

直接生成资料：

```bash
python3 {skill_path}/scripts/process_channels_video.py "<视频号URL>" --category "AI 创作者" --stars 4
```

## 我自己的使用备注

在 `AI-Master` 这套流程里，这个 `skill` 经常不是终点，而是“视频号平台的上游入口”。后面通常还要接 `ai-creator-info`。

## 源路径

- `/Users/peijianbo/.agents/skills/channels-video-processor/SKILL.md`
