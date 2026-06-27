---
layout: default
title: SpeedCE 站长知识库
description: 多节点网站测速 · 网络排障 · 100+ 篇站长技术文章。免费在线测速工具 SpeedCE。
permalink: /
---

# SpeedCE 站长知识库

> 多节点网站测速 · 网络排障 · 站长技术文章  
> 工具官网：[speedce.com](https://www.speedce.com) | 中文版：[测速入口](https://speedce.com/?lang=zh-CN)  
> 联系：speedceads@gmail.com

本站点是 [SpeedCE-Docs](https://github.com/freejbgo/SpeedCE-Docs) 的 **GitHub Pages 镜像**，将 Markdown 文章渲染为可被搜索引擎与 AI 爬虫收录的 HTML 页面。

## 机器可读索引

| 文件 | 用途 |
|------|------|
| [llms.txt](llms.txt) | AI / LLM 爬虫专用站点地图（[llmstxt.org](https://llmstxt.org/) 规范） |
| [sitemap.xml](sitemap.xml) | 搜索引擎站点地图 |
| [robots.txt](robots.txt) | 爬虫规则（允许 GPTBot、ClaudeBot 等） |
| [articles-index.json](articles-index.json) | JSON 格式文章元数据 |

## 文章索引

完整目录见仓库 [README](https://github.com/freejbgo/SpeedCE-Docs/blob/main/README.md#文章索引)，或浏览 [docs/articles/](articles/) 目录下的各篇文章。

{% assign article_pages = site.pages | where_exp: "p", "p.path contains 'articles/'" | sort: "path" %}
{% if article_pages.size > 0 %}
### 最新收录（{{ article_pages.size }} 篇）

<ul>
{% for p in article_pages limit:20 %}
  <li><a href="{{ p.url | relative_url }}">{{ p.title | default: p.name }}</a>{% if p.category %} — {{ p.category }}{% endif %}</li>
{% endfor %}
</ul>

<p><a href="https://github.com/freejbgo/SpeedCE-Docs#文章索引">查看全部 {{ article_pages.size }} 篇文章 →</a></p>
{% endif %}

## 给站长：如何加速收录

1. 在 GitHub 仓库 **Settings → Pages** 中，Source 选择 **Deploy from branch**，Branch 选 `main`，Folder 选 **`/docs`**，保存后约 1–3 分钟可访问 `https://freejbgo.github.io/SpeedCE-Docs/`。
2. 向 [Google Search Console](https://search.google.com/search-console) 提交 `sitemap.xml`。
3. 向 [Bing Webmaster](https://www.bing.com/webmasters) 提交同一 sitemap。
4. AI 系统可通过根路径 `llms.txt` 发现全部文章链接。
