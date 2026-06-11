---
创建日期: 2026-05-14T16:26:36
tags:
  - AI
  - 工具
  - skills
  - B站
简介: 根据 `B` 站空间链接或 `mid` 获取 `UP` 主基础资料，作为上游查询入口。
---

## `bilibili-up-info` 是做什么的

这个 `skill` 用来获取 `B` 站 `UP` 主的基础信息。

它返回的核心字段通常包括：

- `name`
- `intro`
- `avatar_url`
- `space_url`
- `mid`

## 什么时候用

当输入里出现下面这些信息时，就应该想到这个 `skill`：

- `B站`
- 哔哩哔哩
- `UP` 主
- 空间主页
- `mid`
- `https://space.bilibili.com/数字`

## 它只负责什么

它只负责“查询基础资料”，不负责把资料整理成最终的 `Obsidian md`。

如果我最终想把某个 `AI` 创作者沉淀进 `AI-Master`，正确链路是：

1. 先用 `bilibili-up-info` 拿到 `JSON`
2. 再把这份 `JSON` 交给 `ai-creator-info`

## 常用输入

- 纯数字 `mid`
- `B站` 空间主页链接

## 常见输出

输出是一个 `JSON`，例如：

```json
{
  "success": true,
  "mid": "163637592",
  "name": "某位UP主",
  "intro": "个人简介",
  "avatar_url": "https://...",
  "space_url": "https://space.bilibili.com/163637592"
}
```

## 常用命令形态

```bash
python3 {skill_path}/scripts/fetch_bilibili_up_info.py <mid或空间URL>
```

如果需要 `Cookie`：

```bash
python3 {skill_path}/scripts/fetch_bilibili_up_info.py <mid或空间URL> --cookie '你的B站Cookie'
```

## 使用时要注意

- 默认优先返回原始 `JSON`
- 如果用户只是查资料，到这里就可以结束
- 如果用户想生成创作者资料卡，不要在这里停住，要继续接 `ai-creator-info`
- 高频查询或接口风控时，可能需要 `Cookie`

## 我自己的使用备注

在 `AI-Master` 里，这个 `skill` 最常见的定位是“上游查询器”，不是最终落盘器。

## 源路径

- `/Users/peijianbo/.agents/skills/bilibili-up-info/SKILL.md`
