import json, sys, glob

files = [
    "outbox/aws-what-s-new-amazon-s3-tables-variant-iceberg-v3.json",
    "outbox/aws-what-s-new-aws-outposts-asia-pacific-mumbai.json",
    "outbox/cloudflare-changelog-2026-07-09-warp-wifi-network-performance-analytics.json",
    "outbox/openai-news-scientific-computing-agentic-ai.json",
]

for f in files:
    print("===", f, "===")
    d = json.load(open(f))
    print("keys:", list(d.keys()))
    print("slug:", d.get("slug"))
    print("title:", d.get("title"))
    print("body_md len:", len(d.get("body_md", "")))
    print("body_md_en len:", len(d.get("body_md_en", "")))
    print("tags:", d.get("tags"))
    print("emotion:", d.get("emotion"))
    print("importance:", d.get("importance"))
    print("published_at:", d.get("published_at"))
    print("og_title:", d.get("og_title"))
    print("source_name:", d.get("source_name"))
    print("source_url:", d.get("source_url"))
    print()
