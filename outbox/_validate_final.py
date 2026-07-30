import json

VALID_TAGS = {"aws","cloudflare","openai","anthropic","microsoft","ai","ai-safety","security","infrastructure","serverless","devops","web","business","science"}
VALID_EMOTIONS = {"happy","energetic","thinking","smug","confused"}
REQUIRED = ["slug","title","summary","body_md","title_en","summary_en","body_md_en","emotion","importance","source_url","source_name","og_title","tags","published_at"]

with open("work/new_articles.json") as f:
    new_articles = json.load(f)

for a in new_articles:
    slug = a["slug"]
    path = f"outbox/{slug}.json"
    with open(path) as f:
        art = json.load(f)
    problems = []
    missing = [k for k in REQUIRED if k not in art]
    if missing:
        problems.append("missing fields: " + str(missing))
    if art.get("slug") != slug:
        problems.append("slug mismatch")
    if art.get("source_url") != a["url"]:
        problems.append("source_url mismatch")
    if art.get("source_name") != a["source"]:
        problems.append("source_name mismatch")
    if art.get("published_at") != a["published_at"]:
        problems.append("published_at mismatch: " + str(art.get("published_at")) + " vs " + str(a["published_at"]))
    tags = art.get("tags", [])
    bad_tags = [t for t in tags if t not in VALID_TAGS]
    if bad_tags:
        problems.append("bad tags: " + str(bad_tags))
    if not (2 <= len(tags) <= 4):
        problems.append("tag count out of range: " + str(len(tags)))
    if art.get("emotion") not in VALID_EMOTIONS:
        problems.append("bad emotion")
    imp = art.get("importance", 0)
    if not (1 <= imp <= 5):
        problems.append("bad importance")
    if len(art.get("title", "")) > 300:
        problems.append("title too long")
    if len(art.get("summary", "")) > 1000:
        problems.append("summary too long")
    if len(art.get("body_md", "").encode()) > 65536:
        problems.append("body_md too long")
    body = art.get("body_md", "")
    if "!" in body:
        problems.append("half-width ! found in body_md")
    if "?" in body:
        problems.append("half-width ? found in body_md")
    print(slug, "OK" if not problems else problems)
