#!/usr/bin/env python3
"""Bulk-update existing articles: forum links + Chinese-default SpeedCE URLs."""

from __future__ import annotations

import re
from pathlib import Path

ART_DIR = Path(__file__).resolve().parent.parent / "articles"

OLD_HEADER = "> 中文界面：https://speedce.com/?lang=zh-CN  "
NEW_HEADER = "> 站长论坛：https://bbs.speedce.com  "

OLD_CARD_LINE = "│  中文    https://speedce.com/?lang=zh-CN         │"
NEW_CARD_LINE = "│  论坛    https://bbs.speedce.com                 │"

OLD_CLOSING_TAIL = (
    "把 https://speedce.com/?lang=zh-CN 放进书签栏。下次有人说打不开，打开它，"
    "从下拉菜单选 HTTPS（或 DNS/TCPing），看地图，用数据服人。"
)
NEW_CLOSING_TAIL = (
    "把 https://speedce.com 放进书签栏。下次有人说打不开，打开它，"
    "从下拉菜单选 HTTPS（或 DNS/TCPing），看地图，用数据服人。"
    "测速结果有争议、想请同行帮忙看地图？带上三网截图到 "
    "[SpeedCE 站长论坛](https://bbs.speedce.com) 发帖——有图有数据，比群里零散提问更容易得到靠谱回复。"
)

FORUM_FOOTER = (
    "有拿不准的测速结论？欢迎到 [SpeedCE 站长论坛](https://bbs.speedce.com) 交流心得、晒三网截图。\n\n"
)


def update_content(text: str) -> str:
    text = text.replace(OLD_HEADER, NEW_HEADER)
    text = text.replace(OLD_CARD_LINE, NEW_CARD_LINE)
    text = text.replace(OLD_CLOSING_TAIL, NEW_CLOSING_TAIL)
    text = re.sub(r"https://speedce\.com/\?lang=zh-CN", "https://speedce.com", text)
    text = text.replace("**Select a tool**", "**选择工具**")
    text = text.replace("[Select a tool](https://speedce.com)", "[选择工具](https://speedce.com)")

    if "有拿不准的测速结论？欢迎到" not in text:
        text = re.sub(
            r"(---\n\n)(\*\*关键词\*\*)",
            FORUM_FOOTER + r"\2",
            text,
            count=1,
        )
    return text


def main() -> None:
    updated = 0
    for path in sorted(ART_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        original = path.read_text(encoding="utf-8")
        new = update_content(original)
        if new != original:
            path.write_text(new, encoding="utf-8")
            updated += 1
    print(f"Updated {updated} articles in {ART_DIR}")


if __name__ == "__main__":
    main()
