#!/usr/bin/env python3
"""POST outbox/*.json to the blog's ingest API.

On success: adds source_url to state/seen.json and moves the file to
articles/ (archive). On failure: the file stays in outbox/ and the URL is not
marked seen, so the article is regenerated and retried on the next run.

A file that could never survive that retry -- one the parser rejects outright,
or one the API refuses on its content -- is quarantined instead: retrying it is
futile, and because the generator only writes entries that have no outbox file
yet, its presence also blocks the regeneration that would fix it.
"""

import glob
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

from blog_api import ArticleRejected, get_token, post_article
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


# Fields this script itself dereferences. The blog API validates the rest, so
# a file that has these can at least be posted and reported on.
REQUIRED_FIELDS = ("slug", "source_url", "source_name")


def read_article(path: str) -> dict:
    """Load one outbox file. Raises if the file can never be posted as it stands.

    strict=False tolerates raw newlines inside string values -- the generator
    writes body_md with literal newlines instead of \\n escapes often enough to
    matter, and post_article re-serializes with json.dumps, so the wire format
    stays valid either way. Anything the tolerant parse still rejects (a
    generation cut short mid-string, say) is broken beyond repair here.

    Null-valued keys are dropped. The ingest API validates its optional fields
    as "a string if the key is present", so an explicit null is a 400 while
    omitting the key is accepted -- and the generator sometimes emits one for a
    field it invented (og_image, which is not in the prompt's schema at all,
    jammed three articles for a day). Absent and null mean the same thing to
    the API, so send absent.
    """
    with open(path) as f:
        article = json.loads(f.read(), strict=False)
    if not isinstance(article, dict):
        raise TypeError(f"expected an object, got {type(article).__name__}")
    article = {k: v for k, v in article.items() if v is not None}
    missing = [k for k in REQUIRED_FIELDS if not article.get(k)]
    if missing:
        raise KeyError(f"missing {', '.join(missing)}")
    return article


def quarantine(path: str, reason: str) -> None:
    """Take a file that can never be posted as it stands out of the retry loop.

    Underscore-prefixed names are skipped by the publish loop and gitignored, so
    the file leaves the pipeline with this run's workspace and the generator
    recreates the article next run instead of the outbox jamming on it forever.
    """
    name = os.path.basename(path)
    os.rename(path, os.path.join(OUTBOX_DIR, f"_broken-{name}"))
    print(f"error: {name} {reason}; quarantined", file=sys.stderr)


def archive(article: dict, name: str, path: str) -> None:
    """Archive what was actually sent, then drop the outbox copy.

    Not a plain move: the generator's file may hold raw newlines inside strings
    (readable only with strict=False) and nulls that were stripped before the
    POST. articles/ is the archive of record, so keep it strictly parseable and
    equal to the payload the blog received.
    """
    with open(os.path.join(ARCHIVE_DIR, name), "w") as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.remove(path)


def main() -> int:
    # Underscore-prefixed files are scratch the generator left behind, never
    # articles: the blog's slug schema is ^[a-z0-9]+(?:-[a-z0-9]+)*$, so a real
    # article file can never start with one. Skipping them keeps a stray probe
    # out of the retry loop -- a `{"test": true}` leftover once raised KeyError
    # on every run for two days, since a failed file stays in the outbox to be
    # retried and failed again. Quarantined files are given the same prefix, so
    # they are skipped here and, being gitignored (outbox/_*), never committed:
    # the workspace is a fresh checkout each run, so they simply cease to exist
    # and the generator recreates the article from new_articles.json.
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
    quarantined = 0
    published = 0
    for path in files:
        name = os.path.basename(path)
        try:
            article = read_article(path)
        except Exception as e:
            quarantined += 1
            quarantine(path, f"is malformed ({e})")
            continue

        try:
            # Stale leftover from an earlier partially-failed run: the same
            # source_url was already published (possibly under another slug)
            if normalize_url(article["source_url"]) in seen:
                print(f"skip (already published): {name}")
                os.remove(path)
                continue
            stamp_ingest_time(article)
            post_article(token, article)
        except ArticleRejected as e:
            # The content is wrong, so the next attempt fails identically --
            # `"og_image": null` once cost 19 consecutive runs. Drop it and let
            # the generator try again from the source article.
            quarantined += 1
            quarantine(path, f"was rejected ({e})")
            continue
        except Exception as e:
            failures += 1
            print(f"error: failed to post {name}: {e}", file=sys.stderr)
            continue

        seen.add(normalize_url(article["source_url"]))
        # Digest articles cover many upstream items; mark them all as seen
        for url in article.get("covered_urls", []):
            seen.add(normalize_url(url))
        archive(article, name, path)
        published += 1
        print(f"published: {article['slug']} ({article['source_name']})")

    state["seen_urls"] = sorted(seen)
    save_state(state)

    purge_cache(published)

    if failures:
        print(f"{failures}/{len(files)} failed (left in outbox, retried next run)", file=sys.stderr)
    if quarantined:
        print(
            f"{quarantined}/{len(files)} quarantined (unpostable as written, regenerated next run)",
            file=sys.stderr,
        )
    return 1 if failures or quarantined else 0


if __name__ == "__main__":
    sys.exit(main())
