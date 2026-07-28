import json, re

files = [
 "outbox/aws-what-s-new-amazon-s3-tables-variant-iceberg-v3.json",
 "outbox/aws-what-s-new-aws-outposts-asia-pacific-mumbai.json",
 "outbox/cloudflare-changelog-2026-07-09-warp-wifi-network-performance-analytics.json",
 "outbox/openai-news-scientific-computing-agentic-ai.json",
]

VALID_TAGS = {"aws","cloudflare","openai","anthropic","microsoft","ai","ai-safety","security","infrastructure","serverless","devops","web","business","science"}
VALID_EMOTION = {"happy","energetic","thinking","smug","confused"}

for f in files:
    d = json.load(open(f))
    print("==", f)
    for k in ["title","summary","body_md"]:
        v = d[k]
        bad = re.findall(r'[!?]', v)
        if bad:
            print("  HALFWIDTH PUNCT in", k, len(bad))
    for k in ["body_md","body_md_en"]:
        if re.search(r'<[a-zA-Z]', d[k]):
            print("  RAW HTML in", k)
    tags = d["tags"]
    bad_tags = [t for t in tags if t not in VALID_TAGS]
    if bad_tags:
        print("  BAD TAGS", bad_tags)
    if not (1 <= len(tags) <= 4):
        print("  TAG COUNT", len(tags))
    if d["emotion"] not in VALID_EMOTION:
        print("  BAD EMOTION", d["emotion"])
    if not (1 <= d["importance"] <= 5):
        print("  BAD IMPORTANCE", d["importance"])
    print("  title len", len(d["title"]), "summary len", len(d["summary"]), "body len", len(d["body_md"]))
    print("  slug ok:", f.endswith(d["slug"]+".json"))
