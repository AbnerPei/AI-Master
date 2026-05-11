# AI-Master Repo Notes

## Markdown frontmatter

- 在这个项目中，后续新创建的 `.md` 文档，YAML frontmatter 的第一个字段固定写为 `创建日期`。
- 格式固定为 Obsidian `日期 & 时间` 对应的 ISO 时间格式，例如：`创建日期: 2026-05-09T18:08:00`。
- `创建日期` 必须紧跟在 opening `---` 之后，作为 frontmatter 第一项。
- 新文档不要再使用 `date:` 作为首字段；统一使用 `创建日期:`。

示例：

```yaml
---
创建日期: 2026-05-09T18:08:00
tags:
  - git
---
```

## Markdown 语法

- 要求严格执行 Obsidian 支持的 Markdown 语法。
- 正文里出现的英文术语、命令、平台名、代码概念、字段名、关键字等，默认使用反引号包裹。
- 不要写成裸露英文混排，尤其是在中文句子里。

示例：

- 写 `annotated tag` 为什么更适合正式版本，不要写 annotated tag 为什么更适合正式版本。
- 写 例如 `GitHub` / `GitLab` 上，不要写 例如 GitHub / GitLab 上。
- 写 很多初学者容易把 `tag` 当成“另一种分支”。
