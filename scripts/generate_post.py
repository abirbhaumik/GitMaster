#!/usr/bin/env python3
"""Create a new blog post on agentic AI governance and risk management.

Order of preference:
  1. If ANTHROPIC_API_KEY is set, ask Claude to write a fresh post on a topic
     not yet covered.
  2. Otherwise, publish the next pre-written draft from ./queue/.

Run with --force to skip the "at least 2 days since the last post" check.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "posts"
QUEUE = ROOT / "queue"
INTERVAL_DAYS = int(os.environ.get("POST_INTERVAL_DAYS", "2"))
MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)


def parse_front_matter(text: str) -> dict:
    m = FRONT_MATTER.match(text)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    return meta


def existing_posts() -> list[dict]:
    out = []
    for p in sorted(POSTS.glob("*.md")):
        meta = parse_front_matter(p.read_text(encoding="utf-8"))
        meta["file"] = p.name
        out.append(meta)
    return out


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:70].rstrip("-") or "post"


def write_post(today: dt.date, title: str, summary: str, tags: list[str], body: str) -> Path:
    safe = lambda s: s.replace('"', "'").replace("\n", " ").strip()
    path = POSTS / f"{today.isoformat()}-{slugify(title)}.md"
    path.write_text(
        "---\n"
        f'title: "{safe(title)}"\n'
        f"date: {today.isoformat()}\n"
        f'summary: "{safe(summary)}"\n'
        f"tags: {', '.join(safe(t) for t in tags)}\n"
        "---\n\n"
        f"{body.strip()}\n",
        encoding="utf-8",
    )
    return path


SYSTEM = """You write a practitioner blog on governing agentic AI systems: AI agents that \
plan, call tools, and act with some autonomy. Readers are risk, compliance, security and \
engineering leaders. Write with concrete, actionable guidance (controls, checklists, \
examples of failure modes, metrics), not hype. Where you mention regulations or standards \
(EU AI Act, NIST AI RMF, ISO/IEC 42001, etc.) describe them accurately and without \
inventing article numbers, dates or statistics; if unsure, speak in general terms. \
Do not fabricate quotes, studies, or named incidents."""

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
        "body_markdown": {"type": "string"},
    },
    "required": ["title", "summary", "tags", "body_markdown"],
    "additionalProperties": False,
}


def generate_with_claude(posts: list[dict]) -> tuple[str, str, list[str], str]:
    import anthropic

    client = anthropic.Anthropic()
    covered = "\n".join(f"- {p.get('title', p['file'])}" for p in posts[-40:]) or "- (none yet)"
    prompt = f"""Write the next post for the blog.

Already published (do NOT repeat these angles; pick a distinct, useful topic):
{covered}

Requirements:
- 700-1000 words of Markdown in body_markdown. Start with an intro paragraph (no H1 title);
  use ## and ### subheadings, and at least one list or table.
- End with a short "Key takeaways" section.
- summary: one or two sentences for the index page.
- tags: 2-4 short lowercase tags."""

    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
        output_config={"effort": "high", "format": {"type": "json_schema", "schema": SCHEMA}},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    ) as stream:
        msg = stream.get_final_message()

    if msg.stop_reason == "refusal":
        raise RuntimeError("Claude declined the request")
    if msg.stop_reason == "max_tokens":
        raise RuntimeError("Response was cut off (max_tokens)")
    text = next(b.text for b in msg.content if b.type == "text")
    data = json.loads(text)
    return data["title"], data["summary"], data["tags"], data["body_markdown"]


def take_from_queue() -> tuple[str, str, list[str], str] | None:
    drafts = sorted(QUEUE.glob("*.md"))
    if not drafts:
        return None
    draft = drafts[0]
    text = draft.read_text(encoding="utf-8")
    meta = parse_front_matter(text)
    body = FRONT_MATTER.sub("", text, count=1)
    draft.unlink()
    tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    return meta["title"], meta.get("summary", ""), tags, body


def main() -> int:
    force = "--force" in sys.argv
    today = dt.date.today()
    posts = existing_posts()
    if posts and not force:
        last = dt.date.fromisoformat(posts[-1]["date"])
        if (today - last).days < INTERVAL_DAYS:
            print(f"Last post {last}; next one due in {INTERVAL_DAYS - (today - last).days} day(s). Skipping.")
            return 0

    if os.environ.get("ANTHROPIC_API_KEY"):
        print(f"Generating a new post with {MODEL} ...")
        result = generate_with_claude(posts)
    else:
        print("ANTHROPIC_API_KEY not set; using the next queued draft.")
        result = take_from_queue()
        if result is None:
            print("Queue is empty and no API key is configured. Nothing to publish.")
            return 0

    path = write_post(today, *result)
    print(f"Wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
