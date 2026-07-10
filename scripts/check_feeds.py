#!/usr/bin/env python3
"""Detect new articles across the sources defined in sources/*.json.

Standard library only; no LLM involved. When there are new articles, writes
work/new_articles.json and sets has_new=true in GITHUB_OUTPUT.

A source that has not been bootstrapped yet (first run, or just added to
sources/*.json) has all of its current articles marked as seen without being
published, so a newly added site never floods the blog with its backlog; it
is picked up from its next new article onward.

Marking articles as seen after publishing is done by post_articles.py, so a
failed post is retried on the next run.
"""

import json
import os
import re
import sys
import urllib.parse
from datetime import datetime, timezone

from feeds import PARSERS, fetch, load_sources
from paths import DIGEST_ITEMS_PATH, NEW_ARTICLES_PATH, WORK_DIR
from state import load_state, normalize_url, save_state

MAX_NEW_PER_RUN = 20  # articles per run; the overflow is picked up next run


def write_output(key: str, value: str) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"{key}={value}\n")


def derive_slug(source: str, url: str) -> str:
    """Deterministic blog slug from source name + article URL, so regenerating
    the same article always upserts the same slug (no duplicates)."""

    def slugify(s: str) -> str:
        return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")

    segment = urllib.parse.urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]
    # Drop a real page extension only. Matching any ".<alnum>" would also eat
    # the patch number off version tags like "v2.1.206" (-> "v2.1"), collapsing
    # every patch release in a minor onto one slug.
    segment = re.sub(r"\.(html?|php|aspx?|jsp)$", "", segment, flags=re.I)
    return f"{slugify(source)}-{slugify(segment)}"[:120].rstrip("-")


def collect_new_items(sources: list[dict], state: dict) -> tuple[list[dict], list[dict]]:
    """Fetch every source and return (article items, digest groups) of unseen items.

    Bootstraps new sources in place. Digest-mode sources collapse all their new
    items into one group each, later rendered as a single roundup article, so
    they are exempt from MAX_NEW_PER_RUN.
    """
    seen = set(state["seen_urls"])
    bootstrapped = set(state["bootstrapped_sources"])

    new_items: list[dict] = []
    digest_groups: list[dict] = []
    fetched_any = False
    for src in sources:
        try:
            items = PARSERS[src["type"]](fetch(src["url"]), src)
        except Exception as e:  # one failing source must not stop the others
            print(f"warn: failed to fetch {src['name']}: {e}", file=sys.stderr)
            continue
        fetched_any = True

        if src.get("include_path"):
            items = [i for i in items if src["include_path"] in i["url"]]

        if src["name"] not in bootstrapped:
            # First run or newly added source: mark current articles as seen,
            # publish nothing, pick up from the next new article onward
            urls = {normalize_url(i["url"]) for i in items}
            seen |= urls
            bootstrapped.add(src["name"])
            print(f"bootstrap: initialized {src['name']} with {len(urls)} seen articles (nothing published)")
            continue

        unseen = [i for i in items if normalize_url(i["url"]) not in seen]
        if not unseen:
            continue
        if src.get("mode") == "digest":
            digest_groups.append(
                {
                    "source": src["name"],
                    "page_url": src["page_url"],
                    "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "items": unseen,
                }
            )
        else:
            for i in unseen:
                i["slug"] = derive_slug(src["name"], i["url"])
            new_items.extend(unseen)

    if not fetched_any:
        raise RuntimeError("all sources failed")

    state["seen_urls"] = list(seen)
    state["bootstrapped_sources"] = list(bootstrapped)
    return new_items, digest_groups


def cap_and_dedupe(items: list[dict]) -> tuple[list[dict], int]:
    """Dedupe by URL and keep the oldest MAX_NEW_PER_RUN items."""
    dedup = {normalize_url(i["url"]): i for i in items}
    ordered = sorted(dedup.values(), key=lambda i: i["published_at"] or "")
    dropped = max(0, len(ordered) - MAX_NEW_PER_RUN)
    return ordered[:MAX_NEW_PER_RUN], dropped


def main() -> int:
    sources = load_sources()
    state = load_state()

    try:
        new_items, digest_groups = collect_new_items(sources, state)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    save_state(state)

    new_items, dropped = cap_and_dedupe(new_items)

    os.makedirs(WORK_DIR, exist_ok=True)
    with open(NEW_ARTICLES_PATH, "w") as f:
        json.dump(new_items, f, ensure_ascii=False, indent=2)
    with open(DIGEST_ITEMS_PATH, "w") as f:
        json.dump(digest_groups, f, ensure_ascii=False, indent=2)

    has_new = bool(new_items or digest_groups)
    write_output("has_new", "true" if has_new else "false")
    write_output("count", str(len(new_items)))
    print(f"{len(new_items)} new article(s)" + (f" ({dropped} over the cap deferred to next run)" if dropped else ""))
    for i in new_items:
        print(f"  [{i['source']}] {i['title']} — {i['url']}")
    for g in digest_groups:
        print(f"  [digest] {g['source']}: {len(g['items'])} item(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
