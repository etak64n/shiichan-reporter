#!/usr/bin/env python3
"""POST outbox/*.json to the blog's ingest API.

On success: adds source_url to state/seen.json and moves the file to
articles/ (archive). On failure: the file stays in outbox/ and the URL is not
marked seen, so the article is regenerated and retried on the next run.
"""

import glob
import json
import os
import shutil
import sys
import urllib.request
from datetime import datetime, timezone

from blog_api import get_token, post_article
from paths import ARCHIVE_DIR, OUTBOX_DIR
from state import load_state, normalize_url, save_state


def stamp_ingest_time(article: dict) -> None:
    """Date-only sources (e.g. Cloudflare Changelog) give no publish time, so the
    generator stores them at T00:00:00 — which sinks them below same-day articles
    that do have a real time. When such an article is published on its own source
    date, overwrite the time with the current ingest time so it orders by actual
    recency (the blog sorts by published_at, then created_at). Older-dated
    articles (backfill / late catch-up) are left at their source date."""
    pub = article.get("published_at", "")
    now = datetime.now(timezone.utc)
    if pub[11:] == "00:00:00+00:00" and pub[:10] == now.strftime("%Y-%m-%d"):
        article["published_at"] = now.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def purge_cache(published: int) -> None:
    """Purge the Cloudflare edge cache so the edge-cached list pages reflect the
    new articles immediately (the Worker edge-caches /list, /posts, /archive,
    /feed.xml, ... with a long TTL). Best-effort and a no-op unless both
    CF_PURGE_TOKEN and CF_ZONE_ID are set, so it is safe before the secrets
    exist and never blocks publishing."""
    if published <= 0:
        return
    token = os.environ.get("CF_PURGE_TOKEN")
    zone = os.environ.get("CF_ZONE_ID")
    if not token or not zone:
        print("cache purge skipped (CF_PURGE_TOKEN / CF_ZONE_ID not set)")
        return
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/zones/{zone}/purge_cache",
        data=json.dumps({"purge_everything": True}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.load(resp)
        if body.get("success"):
            print("cache purged (purge_everything)")
        else:
            print(f"cache purge failed: {body.get('errors')}", file=sys.stderr)
    except Exception as e:
        print(f"cache purge error: {e}", file=sys.stderr)


def main() -> int:
    # Underscore-prefixed files are scratch the generator left behind, never
    # articles: the blog's slug schema is ^[a-z0-9]+(?:-[a-z0-9]+)*$, so a real
    # article file can never start with one. Skipping them keeps a stray probe
    # out of the retry loop -- a `{"test": true}` leftover once raised KeyError
    # on every run for two days, since a failed file stays in the outbox to be
    # retried and failed again.
    files = [
        p
        for p in sorted(glob.glob(os.path.join(OUTBOX_DIR, "*.json")))
        if not os.path.basename(p).startswith("_")
    ]
    if not files:
        print("outbox is empty; nothing to post")
        return 0

    token = get_token()
    state = load_state()
    seen = set(state["seen_urls"])

    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    failures = 0
    published = 0
    for path in files:
        name = os.path.basename(path)
        try:
            with open(path) as f:
                # strict=False tolerates raw newlines inside string values. The
                # generator writes them unescaped often enough that a strict
                # parse jams the whole pipeline: the bad file stays in the
                # outbox, and the generator skips entries that already have an
                # outbox file, so it is never regenerated either. post_article
                # re-serializes with json.dumps, so the wire format stays valid.
                article = json.loads(f.read(), strict=False)
            # Stale leftover from an earlier partially-failed run: the same
            # source_url was already published (possibly under another slug)
            if normalize_url(article["source_url"]) in seen:
                print(f"skip (already published): {name}")
                os.remove(path)
                continue
            stamp_ingest_time(article)
            post_article(token, article)
        except Exception as e:
            failures += 1
            print(f"error: failed to post {name}: {e}", file=sys.stderr)
            continue

        seen.add(normalize_url(article["source_url"]))
        # Digest articles cover many upstream items; mark them all as seen
        for url in article.get("covered_urls", []):
            seen.add(normalize_url(url))
        shutil.move(path, os.path.join(ARCHIVE_DIR, name))
        published += 1
        print(f"published: {article['slug']} ({article['source_name']})")

    state["seen_urls"] = sorted(seen)
    save_state(state)

    purge_cache(published)

    if failures:
        print(f"{failures}/{len(files)} failed (left in outbox, retried next run)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
