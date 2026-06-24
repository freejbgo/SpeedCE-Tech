#!/usr/bin/env python3
"""Generate root README.md with article index and clickable links."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "articles" / "csdn" / "index.json"
ART_DIR = ROOT / "articles" / "csdn"
README = ROOT / "README.md"

CATEGORY_ORDER = [
    "故障排查", "VPS线路", "CDN", "出海", "行业", "方法论", "对比", "进阶",
]


def extract_intro(md_path: Path, max_len: int = 120) -> str:
    if not md_path.exists():
        return "多节点测速实战长文，以 SpeedCE 为操作示例。"
    text = md_path.read_text(encoding="utf-8")
    # hook after 写在前面
    m = re.search(r"## 写在前面\s*\n+(.+?)(?:\n\n|\n---)", text, re.DOTALL)
    if m:
        intro = m.group(1).strip().replace("\n", " ").replace("**", "")
        # skip duplicate generic line
        if len(intro) > 20:
            if len(intro) > max_len:
                return intro[: max_len - 1] + "…"
            return intro
    return "约 1.6 万字实战长文：场景驱动 + SpeedCE 测速流程 + 检查清单。"


def main():
    articles = json.loads(INDEX.read_text(encoding="utf-8"))
    by_cat: dict[str, list] = {}
    for a in articles:
        by_cat.setdefault(a["category"], []).append(a)

    lines = [
        "# SpeedCE CSDN 文章库\n",
        "\n",
        "> [SpeedCE](https://www.speedce.com) — 多节点网站 / IP 测速工具  \n",
        "> 中文界面：https://speedce.com/?lang=zh-CN  \n",
        "> 联系：speedceads@gmail.com\n",
        "\n",
        "本仓库收录 **210+ 篇** CSDN 高质量长文（每篇约 1.6 万字），",
        "围绕网站测速、故障排查、VPS 验线路、CDN 验收、出海部署等主题。",
        "点击下方标题即可跳转到对应文章正文。\n",
        "\n",
        "## 统计\n",
        "\n",
        f"| 项目 | 数量 |\n|------|------|\n",
        f"| 仓库内长文 | {len(articles)} 篇 |\n",
        "| 每篇配图 | 封面 + 示意图（500/800px） |\n",
        "\n",
        "## 仓库文章目录\n",
    ]

    lines.append("\n> 说明：链接指向本仓库 `articles/csdn/` 下的 Markdown 原文，可直接阅读或复制到 CSDN 发布。\n")

    for cat in CATEGORY_ORDER:
        items = sorted(by_cat.get(cat, []), key=lambda x: x["slug"])
        if not items:
            continue
        lines.append(f"\n### {cat}（{len(items)} 篇）\n\n")
        for a in items:
            slug = a["slug"]
            title = a["title"]
            link = f"articles/csdn/{slug}.md"
            intro = extract_intro(ART_DIR / f"{slug}.md")
            img_cover = f"articles/csdn/images/{slug}/cover-500.png"
            lines.append(f"- [**{title}**]({link})  \n")
            lines.append(f"  {intro}  \n")
            if Path(ROOT / img_cover).exists():
                lines.append(f"  📷 配图：[封面]({img_cover}) · [示意图](articles/csdn/images/{slug}/diagram-500.png)\n\n")
            else:
                lines.append("\n")

    lines.append("\n## 工具与脚本\n\n")
    lines.append("| 脚本 | 用途 |\n|------|------|\n")
    lines.append("| `scripts/premium_article_generator.py` | 生成长文 |\n")
    lines.append("| `scripts/generate_article_images.py` | 生成封面与示意图 |\n")
    lines.append("| `scripts/generate_root_readme.py` | 更新本 README |\n")
    lines.append("\n## 发布建议\n\n")
    lines.append("1. 每 3–5 天发 1 篇，附 SpeedCE 实拍或生成的封面/示意图\n")
    lines.append("2. 文内互链到其他专题文章 + SpeedCE 中文页\n")
    lines.append("3. 详细索引见 [articles/csdn/README.md](articles/csdn/README.md)\n")

    README.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {README} ({len(lines)} sections, {len(articles)} articles)")


if __name__ == "__main__":
    main()
