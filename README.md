# Agentic Governance Notes

A simple static blog on **agentic AI governance and risk management** that publishes a new post every two days.

## How it works

- `posts/`: published posts in Markdown with a small front-matter header.
- `scripts/generate_post.py`: adds a new post if the last one is at least 2 days old.
  - If the `ANTHROPIC_API_KEY` secret is set, Claude writes a fresh post on a topic not yet covered.
  - Otherwise it publishes the next pre-written draft from `queue/`.
- `scripts/build.py`: renders `posts/` into a static site in `_site/` (index, post pages, RSS feed).
- `.github/workflows/publish.yml`: runs daily at 06:17 UTC, generates a post when due, commits it, builds the site and deploys it to GitHub Pages.

## Setup

1. Merge to `main`.
2. In **Settings → Pages**, set **Source** to **GitHub Actions**.
3. (Recommended) In **Settings → Secrets and variables → Actions**, add `ANTHROPIC_API_KEY` so new posts are generated automatically. Without it, the blog runs through the drafts in `queue/` and then stops adding posts.
4. To publish a post immediately, go to **Actions → Publish blog → Run workflow** and tick **force**.

## Run locally

```bash
pip install -r requirements.txt
python scripts/generate_post.py --force   # optional: add a post now
python scripts/build.py
open _site/index.html
```

Optional environment variables: `POST_INTERVAL_DAYS` (default `2`), `CLAUDE_MODEL` (default `claude-opus-5-5`), `SITE_URL` (used in the RSS feed).
