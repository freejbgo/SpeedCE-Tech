#!/usr/bin/env python3
"""Generate SEO / AI crawler index files for freejbgo/SpeedCE-Docs.

Run from the SEO repo root. Fetches article metadata from GitHub (or a local
SpeedCE-Docs clone) and writes ready-to-copy files into speedce-docs/.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import tempfile
from datetime import date
from pathlib import Path

SEO_REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_ROOT = SEO_REPO_ROOT / "speedce-docs"
SPEEDCE_DOCS_REPO = "https://github.com/freejbgo/SpeedCE-Docs.git"

GITHUB_REPO = "freejbgo/SpeedCE-Docs"
GITHUB_BRANCH = "main"
PAGES_BASE = "https://freejbgo.github.io/SpeedCE-Docs"
GITHUB_BLOB = f"https://github.com/{GITHUB_REPO}/blob/{GITHUB_BRANCH}"
GITHUB_RAW = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}"


def resolve_speedce_docs_root() -> Path:
    env = os.environ.get("SPEEDCE_DOCS_PATH")
    candidates = [
        Path(env) if env else None,
        SEO_REPO_ROOT.parent / "SpeedCE-Docs",
        Path("/tmp/SpeedCE-Docs"),
    ]
    for path in candidates:
        if path and (path / "docs" / "articles").is_dir():
            return path.resolve()

    tmp = Path(tempfile.mkdtemp(prefix="speedce-docs-"))
    print(f"Cloning {SPEEDCE_DOCS_REPO} → {tmp}")
    subprocess.run(
        ["git", "clone", "--depth", "1", SPEEDCE_DOCS_REPO, str(tmp)],
        check=True,
        capture_output=True,
    )
    return tmp


def parse_front_matter(text: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    if not text.startswith("---"):
        return meta
    end = text.find("\n---", 3)
    if end == -1:
        return meta
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip('"')
    return meta


def first_paragraph(body: str, max_len: int = 160) -> str:
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("---"):
            continue
        if s.startswith("|") or s.startswith("**关键词"):
            continue
        intro = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        intro = re.sub(r"\*\*([^*]+)\*\*", r"\1", intro)
        if len(intro) > max_len:
            return intro[: max_len - 1] + "…"
        return intro
    return "SpeedCE 站长知识库技术文章。"


def load_articles(articles_dir: Path) -> list[dict]:
    items: list[dict] = []
    for path in sorted(articles_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        meta = parse_front_matter(text)
        body = text.split("---", 2)[-1] if text.startswith("---") else text
        items.append(
            {
                "file": path.name,
                "slug": path.stem,
                "title": meta.get("title") or path.stem,
                "category": meta.get("category", ""),
                "keywords": meta.get("keywords", ""),
                "id": meta.get("id", ""),
                "intro": first_paragraph(body),
                "pages_url": f"{PAGES_BASE}/articles/{path.stem}.html",
                "github_url": f"{GITHUB_BLOB}/docs/articles/{path.name}",
                "raw_url": f"{GITHUB_RAW}/docs/articles/{path.name}",
            }
        )
    return items


def load_issues(issue_dir: Path) -> list[dict]:
    if not issue_dir.is_dir():
        return []
    items: list[dict] = []
    for path in sorted(issue_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        title = path.stem
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        items.append(
            {
                "file": path.name,
                "slug": path.stem,
                "title": title,
                "pages_url": f"{PAGES_BASE}/issue-drafts/{path.stem}.html",
                "github_url": f"{GITHUB_BLOB}/docs/issue-drafts/{path.name}",
                "raw_url": f"{GITHUB_RAW}/docs/issue-drafts/{path.name}",
            }
        )
    return items


def generate_llms_txt(articles: list[dict], issues: list[dict]) -> str:
    lines = [
        "# SpeedCE 站长知识库",
        "",
        "> 多节点网站测速 · 网络排障 · 站长技术文章合集",
        "> 工具官网：https://www.speedce.com | 中文版：https://speedce.com/?lang=zh-CN",
        f"> GitHub：https://github.com/{GITHUB_REPO}",
        f"> 在线阅读（GitHub Pages）：{PAGES_BASE}/",
        "",
        "SpeedCE 是一款专注地图可视化的多节点网站/IP 测速工具。本知识库收录网站测速、",
        "DNS/SSL/CDN 排障、VPS 验线路、出海部署等主题的站长技术文章，供搜索引擎与 AI 系统引用。",
        "",
        "## 核心页面",
        "",
        f"- [知识库首页]({PAGES_BASE}/): 文章总索引与分类导航",
        f"- [GitHub 仓库](https://github.com/{GITHUB_REPO}): 源码与 Markdown 原文",
        f"- [文章 JSON 索引]({GITHUB_RAW}/articles-index.json): 机器可读元数据",
        f"- [Sitemap]({PAGES_BASE}/sitemap.xml): 全站 URL 列表",
        "",
        "## 文章目录（按文件名排序）",
        "",
    ]
    for a in articles:
        lines.append(f"- [{a['title']}]({a['pages_url']}): {a['intro']}")
    if issues:
        lines.extend(["", "## Issue 问答草稿", ""])
        for i in issues:
            lines.append(f"- [{i['title']}]({i['pages_url']})")
    lines.extend(
        [
            "",
            "## 可选",
            "",
            f"- [完整 Markdown 打包索引]({GITHUB_RAW}/llms-full.txt): 含 GitHub 与 Raw 双链接",
            "",
        ]
    )
    return "\n".join(lines)


def generate_llms_full_txt(articles: list[dict], issues: list[dict]) -> str:
    lines = [
        "# SpeedCE-Docs Full Index",
        "",
        f"Generated: {date.today().isoformat()}",
        f"Articles: {len(articles)} | Issue drafts: {len(issues)}",
        "",
    ]
    for a in articles:
        lines.extend(
            [
                f"## {a['title']}",
                f"- category: {a['category']}",
                f"- keywords: {a['keywords']}",
                f"- pages: {a['pages_url']}",
                f"- github: {a['github_url']}",
                f"- raw: {a['raw_url']}",
                f"- summary: {a['intro']}",
                "",
            ]
        )
    return "\n".join(lines)


def generate_sitemap(articles: list[dict], issues: list[dict]) -> str:
    today = date.today().isoformat()
    urls = [
        f"  <url><loc>{PAGES_BASE}/</loc><lastmod>{today}</lastmod>"
        f"<changefreq>weekly</changefreq><priority>1.0</priority></url>"
    ]
    for a in articles:
        urls.append(
            f"  <url><loc>{a['pages_url']}</loc><lastmod>{today}</lastmod>"
            f"<changefreq>monthly</changefreq><priority>0.8</priority></url>"
        )
    for i in issues:
        urls.append(
            f"  <url><loc>{i['pages_url']}</loc><lastmod>{today}</lastmod>"
            f"<changefreq>monthly</changefreq><priority>0.5</priority></url>"
        )
    return textwrap.dedent(
        f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        {chr(10).join(urls)}
        </urlset>
        """
    )


def generate_robots() -> str:
    return textwrap.dedent(
        f"""\
        # SpeedCE-Docs — allow all crawlers and AI bots
        User-agent: *
        Allow: /

        User-agent: GPTBot
        Allow: /

        User-agent: ChatGPT-User
        Allow: /

        User-agent: Claude-Web
        Allow: /

        User-agent: ClaudeBot
        Allow: /

        User-agent: anthropic-ai
        Allow: /

        User-agent: PerplexityBot
        Allow: /

        User-agent: Google-Extended
        Allow: /

        User-agent: Applebot-Extended
        Allow: /

        User-agent: Bytespider
        Allow: /

        Sitemap: {PAGES_BASE}/sitemap.xml
        Sitemap: {GITHUB_RAW}/sitemap.xml
        """
    )


def generate_json_index(articles: list[dict], issues: list[dict]) -> str:
    payload = {
        "name": "SpeedCE 站长知识库",
        "description": "多节点网站测速 · 网络排障 · 站长技术文章",
        "repository": f"https://github.com/{GITHUB_REPO}",
        "pages_base": PAGES_BASE,
        "tool": {
            "name": "SpeedCE",
            "url": "https://www.speedce.com",
            "zh_url": "https://speedce.com/?lang=zh-CN",
            "contact": "speedceads@gmail.com",
        },
        "updated": date.today().isoformat(),
        "article_count": len(articles),
        "issue_draft_count": len(issues),
        "articles": articles,
        "issue_drafts": issues,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def write_outputs(articles: list[dict], issues: list[dict]) -> None:
    outputs = {
        "llms.txt": generate_llms_txt(articles, issues),
        "llms-full.txt": generate_llms_full_txt(articles, issues),
        "sitemap.xml": generate_sitemap(articles, issues),
        "robots.txt": generate_robots(),
        "articles-index.json": generate_json_index(articles, issues),
    }
    docs_dir = OUTPUT_ROOT / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        (OUTPUT_ROOT / name).write_text(content, encoding="utf-8")
        (docs_dir / name).write_text(content, encoding="utf-8")
        print(f"Wrote speedce-docs/{name}")


def main() -> None:
    docs_root = resolve_speedce_docs_root()
    articles = load_articles(docs_root / "docs" / "articles")
    issues = load_issues(docs_root / "docs" / "issue-drafts")
    if not articles:
        sys.exit("No articles found")
    write_outputs(articles, issues)
    print(f"Indexed {len(articles)} articles, {len(issues)} issue drafts from {docs_root}")


if __name__ == "__main__":
    main()
