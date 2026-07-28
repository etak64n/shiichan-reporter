import json, re, sys

files = [
    "outbox/cloudflare-changelog-2026-07-09-warp-wifi-network-performance-analytics.json",
    "outbox/aws-what-s-new-amazon-s3-tables-variant-iceberg-v3.json",
    "outbox/aws-what-s-new-aws-outposts-asia-pacific-mumbai.json",
    "outbox/openai-news-scientific-computing-agentic-ai.json",
]

for f in files:
    print("===", f, "===")
    d = json.load(open(f))
    print("keys:", list(d.keys()))
    for k in ["body_md", "body_md_en", "title", "summary"]:
        v = d[k]
        for m in re.finditer(r"<[a-zA-Z/]", v):
            print(" HTML-like in", k, "at", m.start(), repr(v[max(0, m.start()-20):m.start()+20]))
        for scheme in ["javascript:", "data:", "vbscript:"]:
            if scheme in v:
                print(" BAD SCHEME", scheme, "in", k)
    for k in ["title", "body_md"]:
        v = d[k]
        if "!" in v:
            print(" half-width ! in", k)
        if "?" in v:
            print(" half-width ? in", k)
    print("tags:", d["tags"], "importance:", d["importance"], "emotion:", d["emotion"])
    print("body_md len:", len(d["body_md"]), "body_md_en len:", len(d["body_md_en"]))
    print("title len:", len(d["title"]), "summary len:", len(d["summary"]))
    print()
