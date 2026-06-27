# SpeedCE-Docs SEO / AI 收录包

本目录包含可合并到 [freejbgo/SpeedCE-Docs](https://github.com/freejbgo/SpeedCE-Docs) 的收录文件，帮助搜索引擎与 AI 爬虫发现全部 **100 篇**文章。

## 文件说明

| 路径 | 合并到 SpeedCE-Docs 的位置 | 用途 |
|------|---------------------------|------|
| `llms.txt` | 仓库根目录 + `docs/` | AI 爬虫站点地图（[llmstxt.org](https://llmstxt.org/)） |
| `sitemap.xml` | 仓库根目录 + `docs/` | 搜索引擎 URL 列表 |
| `robots.txt` | 仓库根目录 + `docs/` | 允许 GPTBot、ClaudeBot 等 |
| `articles-index.json` | 仓库根目录 + `docs/` | JSON 元数据索引 |
| `docs/_config.yml` | `docs/_config.yml` | GitHub Pages / Jekyll 配置 |
| `docs/_layouts/default.html` | `docs/_layouts/default.html` | 含 JSON-LD 的 HTML 模板 |
| `docs/index.md` | `docs/index.md` | Pages 首页 |

## 一键同步到 SpeedCE-Docs

在本地克隆两个仓库后执行：

```bash
# 假设目录结构：
# ../SpeedCE-Docs
# ../SEO/speedce-docs  (本目录)

SPEEDCE=../SpeedCE-Docs
SEO=.

cp "$SEO/llms.txt" "$SEO/llms-full.txt" "$SEO/sitemap.xml" "$SEO/robots.txt" "$SEO/articles-index.json" "$SPEEDCE/"
cp "$SEO/docs/"{llms.txt,llms-full.txt,sitemap.xml,robots.txt,articles-index.json,_config.yml,index.md} "$SPEEDCE/docs/"
cp -r "$SEO/docs/_layouts" "$SPEEDCE/docs/"
cp ../SEO/scripts/generate_speedce_docs_seo_index.py "$SPEEDCE/scripts/generate_seo_index.py"
```

## 启用 GitHub Pages（关键一步）

1. 打开 https://github.com/freejbgo/SpeedCE-Docs/settings/pages
2. **Source**: Deploy from a branch
3. **Branch**: `main`，目录选 **`/docs`**
4. 保存后访问 https://freejbgo.github.io/SpeedCE-Docs/

HTML 页面比 GitHub 原始 Markdown 更容易被 Google / Bing / AI 收录。

## 提交到搜索引擎

- Google: https://search.google.com/search-console → 添加 `sitemap.xml`
- Bing: https://www.bing.com/webmasters → 同上

## 重新生成索引

在 SEO 仓库根目录：

```bash
python3 scripts/generate_speedce_docs_seo_index.py
```

脚本会自动 clone SpeedCE-Docs（或使用 `SPEEDCE_DOCS_PATH` 指向本地克隆）并更新本目录。
