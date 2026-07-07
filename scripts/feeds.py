"""Feed fetching and parsing for all supported source types.

Each parser takes (xml_bytes, src) where src is an entry from sources/*.json,
and returns a list of items shaped as:
  {"source": str, "title": str, "url": str, "published_at": str | None}

Source entry (sources/<site>.json is an array of these):
  name         source name (becomes the article's source_name, shown on the blog)
  type         rss | atom | sitemap
  url          feed / sitemap URL
  include_path (sitemap only) treat only URLs containing this substring as articles
"""

import glob
import json
import os
import re
import urllib.parse
import urllib.request
from datetime import timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree

from paths import SOURCES_DIR

UA = "shiichan-reporter/1.0 (+https://blog.shiichan.etak64n.dev)"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read()


def strip_html(text: str, limit: int = 1500) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def normalize_isodate(value: str) -> str | None:
    value = (value or "").strip()
    if not value:
        return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return value + "T00:00:00+00:00"
    return value


def parse_rss(xml_bytes: bytes, src: dict) -> list[dict]:
    root = ElementTree.fromstring(xml_bytes)
    items = []
    for item in root.iter("item"):
        link = (item.findtext("link") or "").strip()
        if not link:
            continue
        published = None
        try:
            pub = item.findtext("pubDate") or ""
            published = parsedate_to_datetime(pub).astimezone(timezone.utc).isoformat()
        except (ValueError, TypeError):
            pass
        items.append(
            {
                "source": src["name"],
                "title": (item.findtext("title") or "").strip(),
                "url": link,
                "published_at": published,
                # Fallback material for the generator when the page itself is unfetchable
                "excerpt": strip_html(item.findtext("description") or ""),
            }
        )
    return items


def parse_atom(xml_bytes: bytes, src: dict) -> list[dict]:
    root = ElementTree.fromstring(xml_bytes)
    items = []
    for entry in root.findall("a:entry", ATOM_NS):
        link = _atom_entry_link(entry)
        if not link:
            continue
        published = normalize_isodate(
            entry.findtext("a:published", "", ATOM_NS) or entry.findtext("a:updated", "", ATOM_NS)
        )
        items.append(
            {
                "source": src["name"],
                "title": (entry.findtext("a:title", "", ATOM_NS) or "").strip(),
                "url": link,
                "published_at": published,
                "excerpt": strip_html(
                    entry.findtext("a:summary", "", ATOM_NS)
                    or entry.findtext("a:content", "", ATOM_NS)
                    or ""
                ),
            }
        )
    return items


def _atom_entry_link(entry: ElementTree.Element) -> str:
    links = entry.findall("a:link", ATOM_NS)
    for link in links:
        if link.get("rel", "alternate") == "alternate":
            return (link.get("href") or "").strip()
    if links:
        return (links[0].get("href") or "").strip()
    return ""


def parse_sitemap(xml_bytes: bytes, src: dict) -> list[dict]:
    """For sites without an official feed. URLs containing include_path count as articles."""
    include_path = src.get("include_path")
    if not include_path:
        raise ValueError(f"{src['name']}: sitemap type requires include_path")
    root = ElementTree.fromstring(xml_bytes)
    items = []
    for url_el in root.findall("sm:url", SITEMAP_NS):
        loc = (url_el.findtext("sm:loc", "", SITEMAP_NS) or "").strip()
        if include_path not in loc:
            continue
        lastmod = normalize_isodate(url_el.findtext("sm:lastmod", "", SITEMAP_NS))
        slug = loc.rstrip("/").rsplit("/", 1)[-1]
        items.append(
            {
                "source": src["name"],
                # Sitemaps carry no title; use a slug-derived placeholder.
                # The generator fetches the real title from the article page.
                "title": slug.replace("-", " "),
                "url": loc,
                "published_at": lastmod,
                "excerpt": "",
            }
        )
    return items


def parse_html_links(html_bytes: bytes, src: dict) -> list[dict]:
    """For sites with no feed at all: extract article links from an index page.

    link_pattern is a regex whose first capture group is the article URL
    (absolute or relative to the page URL). Pages carry no dates, so
    published_at is None; new articles are simply the not-yet-seen links.
    """
    pattern = src.get("link_pattern")
    if not pattern:
        raise ValueError(f"{src['name']}: html type requires link_pattern")
    html = html_bytes.decode("utf-8", errors="replace")
    items = []
    found = set()
    for m in re.finditer(pattern, html):
        url = urllib.parse.urljoin(src["url"], m.group(1))
        if url in found:
            continue
        found.add(url)
        slug = url.rstrip("/").rsplit("/", 1)[-1]
        items.append(
            {
                "source": src["name"],
                # No title in link lists; slug-derived placeholder, real title
                # comes from the article page at generation time
                "title": slug.replace("-", " "),
                "url": url,
                "published_at": None,
                "excerpt": "",
            }
        )
    return items


PARSERS = {
    "rss": parse_rss,
    "atom": parse_atom,
    "sitemap": parse_sitemap,
    "html": parse_html_links,
}


def load_sources() -> list[dict]:
    """Load every source from sources/*.json (one file per site, each an array).

    Files are read in sorted filename order so processing is deterministic.
    """
    files = sorted(glob.glob(os.path.join(SOURCES_DIR, "*.json")))
    if not files:
        raise ValueError(f"no source files found in {SOURCES_DIR}")
    sources: list[dict] = []
    for path in files:
        with open(path) as f:
            entries = json.load(f)
        if isinstance(entries, dict):  # allow a single object per file too
            entries = [entries]
        if not isinstance(entries, list):
            raise ValueError(f"{path}: expected a JSON array of source entries")
        sources.extend(entries)
    for src in sources:
        if src.get("type") not in PARSERS:
            raise ValueError(
                f"{src.get('name')}: unknown type '{src.get('type')}' (valid: {', '.join(PARSERS)})"
            )
        if not src.get("name") or not src.get("url"):
            raise ValueError(f"name and url are required: {src}")
        if src.get("mode", "article") not in ("article", "digest"):
            raise ValueError(f"{src['name']}: mode must be 'article' or 'digest'")
        if src.get("mode") == "digest" and not src.get("page_url"):
            raise ValueError(f"{src['name']}: digest mode requires page_url")
    names = [s["name"] for s in sources]
    if len(names) != len(set(names)):
        raise ValueError("duplicate source name across sources/*.json")
    return sources
