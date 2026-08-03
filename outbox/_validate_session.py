import json, re

files = [
 "outbox/aws-what-s-new-amazon-ec2-i7i-instances-in-additional-regions.json",
 "outbox/aws-what-s-new-amazon-gamelift-streams.json",
 "outbox/cloudflare-blog-grpc-workers.json",
 "outbox/cloudflare-blog-python-workers-rpc.json",
 "outbox/cloudflare-changelog-2026-08-03-python-javascript-rpc.json",
]

new_articles = json.load(open("work/new_articles.json"))
by_slug = {a["slug"]: a for a in new_articles}

VALID_TAGS = {"aws","cloudflare","openai","anthropic","microsoft","ai","ai-safety","security","infrastructure","serverless","devops","web","business","science"}
VALID_EMOTION = {"happy","energetic","thinking","smug","confused"}

for f in files:
    d = json.load(open(f))
    slug = d["slug"]
    src = by_slug.get(slug)
    print("====", f)
    if not src:
        print("  !! slug not found in new_articles.json")
        continue
    problems = []
    if d.get("source_url") != src["url"]:
        problems.append("source_url mismatch: " + str(d.get("source_url")) + " vs " + src["url"])
    if d.get("source_name") != src["source"]:
        problems.append("source_name mismatch: " + str(d.get("source_name")) + " vs " + src["source"])
    if src.get("published_at") and d.get("published_at") != src["published_at"]:
        problems.append("published_at mismatch: " + str(d.get("published_at")) + " vs " + str(src["published_at"]))
    for k in ["slug","title","summary","body_md","title_en","summary_en","body_md_en","emotion","importance","source_url","source_name","og_title","tags","published_at"]:
        if k not in d:
            problems.append("missing key " + k)
    if d.get("emotion") not in VALID_EMOTION:
        problems.append("invalid emotion " + str(d.get("emotion")))
    imp = d.get("importance")
    if not isinstance(imp, int) or not (1 <= imp <= 5):
        problems.append("invalid importance " + str(imp))
    tags = d.get("tags", [])
    if not (2 <= len(tags) <= 4):
        problems.append("tag count " + str(len(tags)))
    for t in tags:
        if t not in VALID_TAGS:
            problems.append("invalid tag " + t)
    body = d.get("body_md","")
    if re.search(r'<[a-zA-Z]', body):
        problems.append("possible raw HTML tag in body_md")
    body_en = d.get("body_md_en","")
    if re.search(r'<[a-zA-Z]', body_en):
        problems.append("possible raw HTML tag in body_md_en")
    if '!' in body or '?' in body:
        problems.append("half-width EXCLAIM or QUESTION found in body_md")
    if len(body) < 100:
        problems.append("body_md suspiciously short")
    print("  len body_md:", len(body), "len body_md_en:", len(body_en))
    print("  tags:", tags, "importance:", imp, "emotion:", d.get("emotion"))
    if problems:
        for p in problems:
            print("  ISSUE:", p)
    else:
        print("  OK")
