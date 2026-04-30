---
source_url: https://x.com/karpathy/status/2039805659525644595
ingested: 2026-04-30
sha256: 8e0c34e2f5511f034ae0f6089040c3d0038d8e98798f669fe114dd93509845c4
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

## 中文翻译

LLM 知识库

我最近发现一件非常有用的事情：用 LLM 为自己感兴趣的不同研究主题构建个人知识库。这样一来，我近期很大一部分 token 吞吐量不再主要用于操作代码，而是更多用于操作知识；这些知识以 Markdown 和图片的形式存储。最新的 LLM 在这件事上已经相当擅长。具体来说：

数据导入：
我会把源文档（文章、论文、代码仓库、数据集、图片等）索引到 `raw/` 目录中，然后用 LLM 增量地“编译”一个 wiki。这个 wiki 本质上就是按目录结构组织的一组 `.md` 文件。wiki 会包含对 `raw/` 中所有数据的摘要、反向链接，并进一步把资料分类到不同概念下，为这些概念撰写文章，再把它们互相链接起来。为了把网页文章转换为 `.md` 文件，我喜欢使用 Obsidian Web Clipper 扩展；此外我也会用一个快捷键把相关图片全部下载到本地，这样我的 LLM 就能方便地引用这些图片。

IDE：
我把 Obsidian 当作 IDE 的“前端”，用它来查看原始数据、编译后的 wiki 和派生出来的可视化内容。需要注意的是，LLM 会负责写入并维护 wiki 的所有数据，我自己很少直接编辑它。我也试过一些 Obsidian 插件，用其他方式渲染和查看数据，比如用 Marp 做幻灯片。

问答：
真正有意思的地方在于，当你的 wiki 足够大之后（比如我最近某些研究方向的 wiki 大约有 100 篇文章、40 万词），你就可以让 LLM agent 围绕这个 wiki 回答各种复杂问题，它会自己去研究答案等等。我本来以为必须上复杂的 RAG，但在这种“小规模”下，LLM 已经很擅长自动维护索引文件和各文档的简短摘要，并且能比较容易地读取所有重要的相关资料。

输出：
我不喜欢只在文本或终端里拿到答案，而是更喜欢让它为我渲染 Markdown 文件、Marp 格式的幻灯片，或者 matplotlib 图片；这些输出我随后又会在 Obsidian 中查看。根据问题不同，你可以想象出许多其他可视化输出格式。很多时候，我最后会把这些输出重新“归档”回 wiki，用来增强后续查询能力。这样，我自己的探索和提问都会在知识库里持续累积。

Linting：
我也会对 wiki 运行一些 LLM “健康检查”，例如找出不一致的数据、用网页搜索补齐缺失数据、发现有意思的连接并作为新文章候选等，从而逐步清理 wiki，提升整体数据完整性。LLM 很擅长建议下一步可以提出和深入的问题。

额外工具：
我发现自己还会开发额外工具来处理这些数据。例如，我 vibe coded 了一个小而朴素的 wiki 搜索引擎。我既会直接在 Web UI 里使用它，但更多时候，我希望把它作为 CLI 工具交给 LLM，让它在更大的查询任务中调用。

进一步探索：
随着仓库增长，一个自然的想法是进一步考虑合成数据生成和微调，让你的 LLM 不只是通过上下文窗口“看到”这些数据，而是真正把这些数据“知道”到模型权重里。

总结：来自一定数量来源的 raw data 被收集起来，然后由 LLM 编译成 `.md` wiki，再由 LLM 通过各种 CLI 对它进行问答和增量增强，所有内容都可以在 Obsidian 中查看。你很少需要亲手写或编辑这个 wiki，它是 LLM 的领域。我认为这里有机会诞生一个非常棒的新产品，而不只是现在这种 hacky 的脚本集合。

## Local Notes

- 这篇长帖直接描述了用 LLM 维护个人知识库的完整闭环：原始资料进入 `raw/`，LLM 增量编译 Markdown wiki，Obsidian 作为阅读/编辑/可视化前端，之后再通过 Q&A、可视化输出、lint/health check、工具扩展和潜在微调继续增强知识库。
- 本资料与当前 AI-Master 知识库的组织方式高度相关，可作为后续完善 `raw/`、`wiki/`、source manifest、lint、查询归档和 Obsidian 工作流的参考来源。
