---
title: B站 AI 创作者技能快速导入
created: 2026-05-01
updated: 2026-05-01
type: playbook
tags: [ai, tooling, workflow, automation, playbook]
sources: []
confidence: high
status: active
---

# B站 AI 创作者技能快速导入

这份操作手册用于备忘 `ai-creator-info` 和 `bilibili-up-info` 两个 skill 的恢复、依赖安装和使用流程。它属于 [[LLM Wiki]] 的整理层，不是外部原始资料，因此放在 `wiki/P_Playbooks(操作手册)/`。

## 这两个 skill 是什么关系

```text
B站空间 URL / mid
        |
        v
bilibili-up-info
        |
        | 获取 UP 主 JSON
        v
ai-creator-info
        |
        | 使用已获取 JSON 生成 Obsidian md
        v
raw/{分类目录}/AI 创作者 - {UP主名}.md
```

- `bilibili-up-info`：负责联网查询 B 站 UP 主资料。
- `ai-creator-info`：负责把已经查询到的 JSON 生成 Obsidian 风格 md。
- 正确流程是：先查询 JSON，再用 JSON 生成 md。
- 不要在生成 md 阶段再次联网查询，避免重复请求和 B 站风控。

## 源目录

当前这两个 skill 的源文件在：

```text
/Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/bilibili-up-info
/Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/ai-creator-info
```

关键脚本：

```text
/Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/bilibili-up-info/scripts/fetch_bilibili_up_info.py
/Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/ai-creator-info/scripts/generate_profile.py
```

## 恢复到 .agents/skills

如果以后 `.agents/skills` 里的软链接被删了，手动执行：

```bash
mkdir -p /Users/peijianbo/.agents/skills

ln -s /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/bilibili-up-info /Users/peijianbo/.agents/skills/bilibili-up-info
ln -s /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/ai-creator-info /Users/peijianbo/.agents/skills/ai-creator-info
```

验证：

```bash
ls -la /Users/peijianbo/.agents/skills
```

应该能看到：

```text
bilibili-up-info -> /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/bilibili-up-info
ai-creator-info -> /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/ai-creator-info
```

## 安装依赖

两个 skill 的 Python 依赖都很轻，主要是：

```text
requests>=2.25.0
```

安装方式：

```bash
python3 -m pip install requests
```

或分别按 requirements 安装：

```bash
python3 -m pip install -r /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/bilibili-up-info/requirements.txt
python3 -m pip install -r /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/ai-creator-info/requirements.txt
```

说明：

- `bilibili-up-info` 需要 `requests`，因为它要请求 B 站接口。
- `ai-creator-info` 当前脚本只解析 JSON 并写 md，理论上不需要第三方库；但为了完整 skill 流程，保留同样的 requirements。

## 第一步：查询 B 站 UP 主 JSON

命令格式：

```bash
python3 /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/bilibili-up-info/scripts/fetch_bilibili_up_info.py <B站空间URL或mid>
```

示例：

```bash
python3 /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/bilibili-up-info/scripts/fetch_bilibili_up_info.py https://space.bilibili.com/474921808
```

成功输出示例：

```json
{
  "success": true,
  "mid": "474921808",
  "name": "code秘密花园",
  "intro": "叫我花园老师吧，关注我一起玩转 AI",
  "avatar_url": "https://i1.hdslb.com/bfs/face/78046c565ac64613387671d5138f0c623efda405.jpg",
  "space_url": "https://space.bilibili.com/474921808"
}
```

如果被 B 站风控，可能会看到：

```json
{
  "success": false,
  "mid": "341376543",
  "error": "WBI 接口失败：B 站接口返回失败 code=-352..."
}
```

这种情况先不要生成 md，可以稍后重试，或提供 Cookie。

## 可选：带 Cookie 查询

直接传 Cookie：

```bash
python3 /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/bilibili-up-info/scripts/fetch_bilibili_up_info.py <B站空间URL或mid> --cookie '你的B站Cookie'
```

用环境变量：

```bash
export BILIBILI_COOKIE='你的B站Cookie'
python3 /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/bilibili-up-info/scripts/fetch_bilibili_up_info.py <B站空间URL或mid>
```

## 第二步：确认分类和星级

分类规则：

```text
1. AI 大神
2. AI 创作者
3. 两者都是
```

星级：

```text
1-5 星，默认 4 星
```

常用输入：

```text
2，3
```

表示：

- 分类：AI 创作者
- 星级：3 星

## 第三步：使用 JSON 生成 md

命令格式：

```bash
python3 /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/ai-creator-info/scripts/generate_profile.py \
  --json '<上一步完整 JSON>' \
  --category "AI 创作者" \
  --stars 3
```

示例：

```bash
python3 /Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/ai-creator-info/scripts/generate_profile.py \
  --json '{"success": true, "mid": "474921808", "name": "code秘密花园", "intro": "叫我花园老师吧，关注我一起玩转 AI", "avatar_url": "https://i1.hdslb.com/bfs/face/78046c565ac64613387671d5138f0c623efda405.jpg", "space_url": "https://space.bilibili.com/474921808"}' \
  --category "AI 创作者" \
  --stars 3
```

默认输出到当前目录的：

```text
raw/A_AI-Content-Creator(AI 创作者)/AI 创作者 - {UP主名}.md
raw/A_AI-Gurus(AI大神)/AI 大神 - {UP主名}.md
```

## 当前 Codex 里的推荐使用方式

以后在 Codex 中可以直接输入：

```text
[$ai-creator-info](/Users/peijianbo/Documents/AbnerPei/GitHub/niche-skills/B站/ai-creator-info/SKILL.md) https://space.bilibili.com/xxxx
```

或者直接给 B 站空间链接：

```text
https://space.bilibili.com/xxxx
```

正确处理流程应该是：

1. 先调用 `bilibili-up-info` 查询 JSON。
2. 把 JSON 原样展示出来。
3. 询问分类和星级。
4. 复用上一步 JSON 生成 md。
5. 不要在第 4 步重新联网查询。

## 常见问题

### 1. 为什么要分成两个 skill？

因为职责不同：

- `bilibili-up-info` 只负责“查资料”。
- `ai-creator-info` 只负责“生成资料文档”。

这样可以先让用户确认原始 JSON，再决定分类和星级。

### 2. 为什么生成 md 时要复用 JSON？

因为 B 站接口容易风控。如果查询阶段已经拿到了 JSON，生成阶段再联网一次没有必要，还可能失败。

### 3. 如果查询失败还能生成吗？

可以，但必须手动提供等价 JSON，至少包含：

```json
{
  "success": true,
  "mid": "UP主mid",
  "name": "UP主昵称",
  "intro": "UP主简介",
  "avatar_url": "头像URL",
  "space_url": "B站空间URL"
}
```

### 4. 如果软链接被删了怎么办？

回到本文“恢复到 .agents/skills”一节，重新执行 `ln -s` 命令即可。

### 5. 如果源仓库移动了怎么办？

先找到新的 `SKILL.md`：

```bash
find /Users/peijianbo/Documents -path '*bilibili-up-info/SKILL.md' -o -path '*ai-creator-info/SKILL.md'
```

然后用新的源路径重新建立软链接。

## Related

- [[LLM Wiki]]
- [[AI 资源索引]]
