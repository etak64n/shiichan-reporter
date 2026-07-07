"""Repository layout constants shared by the scripts."""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# One JSON file per site, each an array of source entries
SOURCES_DIR = os.path.join(ROOT, "sources")
STATE_PATH = os.path.join(ROOT, "state", "seen.json")
WORK_DIR = os.path.join(ROOT, "work")
NEW_ARTICLES_PATH = os.path.join(WORK_DIR, "new_articles.json")
DIGEST_ITEMS_PATH = os.path.join(WORK_DIR, "digest_items.json")
OUTBOX_DIR = os.path.join(ROOT, "outbox")
ARCHIVE_DIR = os.path.join(ROOT, "articles")
