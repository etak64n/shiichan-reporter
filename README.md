# sheechan-reporter

Bot that watches the tech blogs defined in `sources.json` (initially AWS /
Anthropic / OpenAI / Cloudflare), writes Japanese introduction articles for new
posts with Claude Code (subscription quota, no API billing), and publishes them
fully automatically to [blog.shiichan.etak64n.dev](https://blog.shiichan.etak64n.dev).

## How it works

```
GitHub Actions (daily at 10:07 JST)
  ├─ scripts/check_feeds.py   … diff RSS/atom/sitemap sources against state/seen.json (no LLM)
  ├─ claude-code-action       … generate outbox/*.json per prompts/generate.md (setup-token / subscription)
  ├─ scripts/post_articles.py … POST with an OIDC token → mark seen → archive to articles/
  └─ git commit               … persist state and the article archive
```

- Runs with no new articles never start Claude, so they consume no subscription quota
- A failed post is not marked seen and is retried automatically on the next run
- `articles/` is an archive of every published article — a backup of the blog's D1
  (the whole blog can be restored by re-POSTing them)
- At most 10 articles are generated per run; the overflow carries over to the next day
- Manual trigger: Actions tab → watch → Run workflow

## Setup

1. Push this repository as `etak64n/sheechan-reporter`. The blog pins
   `ALLOWED_OIDC_SUB` to `repo:etak64n/sheechan-reporter:ref:refs/heads/main`,
   so renaming the repo requires updating the blog's wrangler.jsonc too
2. Run `claude setup-token` locally (Pro/Max subscription, valid for 1 year) and
   store the token as the repository secret `CLAUDE_CODE_OAUTH_TOKEN`
3. The initial seen state is committed (`state/seen.json`); only articles
   published after that are picked up

## Adding a monitored site

1. Add one entry to `sources.json`:

   ```json
   { "name": "GitHub", "type": "atom", "url": "https://github.blog/feed/" }
   ```

   - `type` is `rss` / `atom` / `sitemap` / `html`
   - `include_path` (any type): only URLs containing this substring count as
     articles (required for `sitemap`, e.g. Anthropic's `"/news/"`)
   - `link_pattern` (`html` only): regex whose first capture group is the
     article URL, for sites with no feed at all
   - `mode: "digest"` (with `page_url`): for high-volume sources (e.g. AWS
     What's New at ~7/day) all new items are rolled into ONE daily roundup
     article instead of one article each; exempt from the per-run cap
   - `name` is shown on the blog as the article's source
2. Add the new site's domain to `ALLOWED_SOURCE_HOSTS` in the blog's
   wrangler.jsonc and deploy
3. Just push. **A newly added site never floods the blog with its backlog**:
   an unbootstrapped source has its current articles marked seen and is picked
   up from its next new article onward

To remove a source, delete its entry from sources.json; leftover history in
`state/seen.json` is harmless.

## Removing a published article

See the blog's README (`DELETE /api/articles/:slug`). To keep a removed
article from being re-posted, make sure its URL is still present in
`state/seen.json` (if it is, it will not be regenerated).

## Local testing

```sh
python3 scripts/check_feeds.py            # inspect work/new_articles.json
BLOG_DEV_TOKEN=xxx BLOG_API_URL=http://localhost:8787 python3 scripts/post_articles.py
# on the blog side, put DEV_BEARER_TOKEN=xxx in .dev.vars and run wrangler dev
```
