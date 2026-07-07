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

from blog_api import get_token, post_article
from paths import ARCHIVE_DIR, OUTBOX_DIR
from state import load_state, normalize_url, save_state


def main() -> int:
    files = sorted(glob.glob(os.path.join(OUTBOX_DIR, "*.json")))
    if not files:
        print("outbox is empty; nothing to post")
        return 0

    token = get_token()
    state = load_state()
    seen = set(state["seen_urls"])

    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    failures = 0
    for path in files:
        name = os.path.basename(path)
        try:
            with open(path) as f:
                article = json.load(f)
            # Stale leftover from an earlier partially-failed run: the same
            # source_url was already published (possibly under another slug)
            if normalize_url(article["source_url"]) in seen:
                print(f"skip (already published): {name}")
                os.remove(path)
                continue
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
        print(f"published: {article['slug']} ({article['source_name']})")

    state["seen_urls"] = sorted(seen)
    save_state(state)

    if failures:
        print(f"{failures}/{len(files)} failed (left in outbox, retried next run)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
