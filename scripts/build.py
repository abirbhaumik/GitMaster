#!/usr/bin/env python3
"""Build the static site from posts/*.md into _site/."""
from __future__ import annotations

import datetime as dt
import html
import os
import shutil
from pathlib import Path

import markdown

from generate_post import FRONT_MATTER, parse_front_matter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
SITE_TITLE = "Agentic Governance Notes"
SITE_TAGLINE = "Governance and risk management for agentic AI, with a new post every two days."
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")


def page(title: str, body: str, depth: int = 0) -> str:
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{up}style.css">
<link rel="alternate" type="application/rss+xml" title="{SITE_TITLE}" href="{up}feed.xml">
</head>
<body>
<header class="site"><a class="brand" href="{up}index.html">{SITE_TITLE}</a>
<nav><a href="{up}index.html">Posts</a><a href="{up}feed.xml">RSS</a></nav></header>
<main>
{body}
</main>
<footer>Posts are drafted with AI assistance. They are general information, not legal advice.</footer>
</body>
</html>
"""


def nice_date(d: str) -> str:
    return dt.date.fromisoformat(d).strftime("%B %-d, %Y")


def tag_html(tags: str) -> str:
    return "".join(f'<span class="tag">{html.escape(t.strip())}</span>' for t in tags.split(",") if t.strip())


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "posts").mkdir(parents=True)
    shutil.copy(ROOT / "static" / "style.css", OUT / "style.css")

    posts = []
    for p in sorted((ROOT / "posts").glob("*.md"), reverse=True):
        text = p.read_text(encoding="utf-8")
        meta = parse_front_matter(text)
        body_md = FRONT_MATTER.sub("", text, count=1)
        meta["html"] = markdown.markdown(body_md, extensions=["tables", "fenced_code"])
        meta["slug"] = p.stem
        posts.append(meta)

    for i, m in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        nav = '<nav class="pager">'
        nav += f'<a href="{older["slug"]}.html">&larr; {html.escape(older["title"])}</a>' if older else "<span></span>"
        nav += f'<a href="{newer["slug"]}.html">{html.escape(newer["title"])} &rarr;</a>' if newer else "<span></span>"
        nav += "</nav>"
        body = f"""<article>
<p class="meta">{nice_date(m["date"])} {tag_html(m.get("tags", ""))}</p>
<h1>{html.escape(m["title"])}</h1>
{m["html"]}
</article>
{nav}"""
        (OUT / "posts" / f"{m['slug']}.html").write_text(page(m["title"], body, depth=1), encoding="utf-8")

    items = "\n".join(
        f"""<li class="card"><p class="meta">{nice_date(m["date"])} {tag_html(m.get("tags", ""))}</p>
<h2><a href="posts/{m["slug"]}.html">{html.escape(m["title"])}</a></h2>
<p>{html.escape(m.get("summary", ""))}</p></li>"""
        for m in posts
    )
    index = f"""<section class="hero"><h1>{SITE_TITLE}</h1><p>{SITE_TAGLINE}</p></section>
<ul class="posts">
{items}
</ul>"""
    (OUT / "index.html").write_text(page(SITE_TITLE, index), encoding="utf-8")

    rss_items = "".join(
        f"""<item><title>{html.escape(m["title"])}</title>
<link>{SITE_URL}/posts/{m["slug"]}.html</link><guid>{SITE_URL}/posts/{m["slug"]}.html</guid>
<pubDate>{dt.date.fromisoformat(m["date"]).strftime("%a, %d %b %Y 00:00:00 +0000")}</pubDate>
<description>{html.escape(m.get("summary", ""))}</description></item>"""
        for m in posts[:20]
    )
    (OUT / "feed.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>{SITE_TITLE}</title><link>{SITE_URL}/</link>
<description>{SITE_TAGLINE}</description>{rss_items}</channel></rss>
""",
        encoding="utf-8",
    )
    print(f"Built {len(posts)} posts into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
