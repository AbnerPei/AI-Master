---
source_url: https://x.com/karpathy/status/2039805659525644595
ingested: 2026-04-30
sha256: e075e8cccaa01f9f865bf436a2aaa3ed43652d4665786728e279a391179ee2ef
source_type: article
title: LLM Knowledge Bases
author: Andrej Karpathy
author_handle: karpathy
author_url: https://x.com/karpathy
published_at: "2026-04-02T20:42:21Z"
retrieved_at: "2026-04-30"
platform: X / Twitter
source_id: "2039805659525644595"
language: en
tags: [ai, llm, rag, tooling, workflow, automation, source]
category: 重量级文章
classification: [knowledge-base, llm-wiki, obsidian, markdown, personal-knowledge-management]
---

# LLM Knowledge Bases

## Source Metadata

| Field | Value |
|---|---|
| Title | LLM Knowledge Bases |
| Author | Andrej Karpathy (@karpathy) |
| Author URL | https://x.com/karpathy |
| Source URL | https://x.com/karpathy/status/2039805659525644595 |
| Platform | X / Twitter |
| Published at | Thu Apr 02 20:42:21 +0000 2026 |
| Retrieved at | 2026-04-30 |
| Language | en |
| Source type | article / long-form X post |
| Category | 重量级文章；知识库方法论；LLM 工具链；Obsidian / Markdown 工作流 |
| Engagement at retrieval | likes 57923, retweets 6972, replies 2827, quotes 2043, bookmarks 104705, views 20751061 |

## Tags

- ai
- llm
- rag
- tooling
- workflow
- automation
- source

## Classification

- Raw directory: `raw/A_Articles(文章)/I_Important-Articles(重量级文章)/`
- Knowledge theme: LLM-assisted personal knowledge bases
- Related entities: Andrej Karpathy
- Related concepts: LLM wiki, raw/source layer, compiled Markdown wiki, Obsidian frontend, knowledge-base linting, wiki Q&A, synthetic data / fine-tuning

## Original Text

LLM Knowledge Bases

Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest. In this way, a large fraction of my recent token throughput is going less into manipulating code, and more into manipulating knowledge (stored as markdown and images). The latest LLMs are quite good at it. So:

Data ingest:
I index source documents (articles, papers, repos, datasets, images, etc.) into a raw/ directory, then I use an LLM to incrementally "compile" a wiki, which is just a collection of .md files in a directory structure. The wiki includes summaries of all the data in raw/, backlinks, and then it categorizes data into concepts, writes articles for them, and links them all. To convert web articles into .md files I like to use the Obsidian Web Clipper extension, and then I also use a hotkey to download all the related images to local so that my LLM can easily reference them.

IDE:
I use Obsidian as the IDE "frontend" where I can view the raw data, the the compiled wiki, and the derived visualizations. Important to note that the LLM writes and maintains all of the data of the wiki, I rarely touch it directly. I've played with a few Obsidian plugins to render and view data in other ways (e.g. Marp for slides).

Q&A:
Where things get interesting is that once your wiki is big enough (e.g. mine on some recent research is ~100 articles and ~400K words), you can ask your LLM agent all kinds of complex questions against the wiki, and it will go off, research the answers, etc. I thought I had to reach for fancy RAG, but the LLM has been pretty good about auto-maintaining index files and brief summaries of all the documents and it reads all the important related data fairly easily at this ~small scale.

Output:
Instead of getting answers in text/terminal, I like to have it render markdown files for me, or slide shows (Marp format), or matplotlib images, all of which I then view again in Obsidian. You can imagine many other visual output formats depending on the query. Often, I end up "filing" the outputs back into the wiki to enhance it for further queries. So my own explorations and queries always "add up" in the knowledge base.

Linting:
I've run some LLM "health checks" over the wiki to e.g. find inconsistent data, impute missing data (with web searchers), find interesting connections for new article candidates, etc., to incrementally clean up the wiki and enhance its overall data integrity. The LLMs are quite good at suggesting further questions to ask and look into.

Extra tools:
I find myself developing additional tools to process the data, e.g. I vibe coded a small and naive search engine over the wiki, which I both use directly (in a web ui), but more often I want to hand it off to an LLM via CLI as a tool for larger queries. 

Further explorations:
As the repo grows, the natural desire is to also think about synthetic data generation + finetuning to have your LLM "know" the data in its weights instead of just context windows.

TLDR: raw data from a given number of sources is collected, then compiled by an LLM into a .md wiki, then operated on by various CLIs by the LLM to do Q&A and to incrementally enhance the wiki, and all of it viewable in Obsidian. You rarely ever write or edit the wiki manually, it's the domain of the LLM. I think there is room here for an incredible new product instead of a hacky collection of scripts.

## Local Notes

- 这篇长帖直接描述了用 LLM 维护个人知识库的完整闭环：原始资料进入 `raw/`，LLM 增量编译 Markdown wiki，Obsidian 作为阅读/编辑/可视化前端，之后再通过 Q&A、可视化输出、lint/health check、工具扩展和潜在微调继续增强知识库。
- 本资料与当前 AI-Master 知识库的组织方式高度相关，可作为后续完善 `raw/`、`wiki/`、source manifest、lint、查询归档和 Obsidian 工作流的参考来源。
