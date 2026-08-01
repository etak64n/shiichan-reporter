import json, re

VALID_TAGS = {"aws","cloudflare","openai","anthropic","microsoft",
              "ai","ai-safety","security","infrastructure","serverless","devops","web","business","science"}
VALID_EMOTION = {"happy","energetic","thinking","smug","confused"}

new_articles = json.load(open("work/new_articles.json"))
by_slug = {a["slug"]: a for a in new_articles}

files = ["outbox/cloudflare-changelog-2026-07-24-r2-sippy-azure-s3-compatible-support.json",
         "outbox/cloudflare-changelog-2026-07-30-rotate-stream-broadcast-keys.json",
         "outbox/openai-news-disrupting-malicious-uses-of-ai-scam-operations.json"]

for f in files:
    d = json.load(open(f))
    src = by_slug.get(d["slug"])
    print("===", f)
    if not src:
        print("  !! slug not found in new_articles.json")
        continue
    if d["source_url"] != src["url"]:
        print("  !! source_url mismatch", d["source_url"], src["url"])
    if d["source_name"] != src["source"]:
        print("  !! source_name mismatch")
    if d["og_title"] != src["title"]:
        print("  note og_title differs from feed title:", d["og_title"], "|", src["title"])
    if d["published_at"] != src["published_at"]:
        print("  !! published_at mismatch", d["published_at"], src["published_at"])
    if d["emotion"] not in VALID_EMOTION:
        print("  !! invalid emotion", d["emotion"])
    if not (1 <= d["importance"] <= 5):
        print("  !! invalid importance", d["importance"])
    bad_tags = [t for t in d["tags"] if t not in VALID_TAGS]
    if bad_tags:
        print("  !! invalid tags", bad_tags)
    if not (2 <= len(d["tags"]) <= 4):
        print("  !! tag count out of range", d["tags"])
    for field in ["body_md","body_md_en"]:
        text = d[field]
        if re.search(r'[!?]', text):
            print("  !! half-width !/? found in", field)
        if re.search(r'<[a-zA-Z/]', text):
            print("  !! raw HTML-like tag found in", field)
    for field in ["title","summary","body_md"]:
        text = d[field]
        for m in re.finditer(r'([ぁ-んァ-ン一-龯])([A-Za-z0-9])|([A-Za-z0-9])([ぁ-んァ-ン一-龯])', text):
            print("  !! possible missing half-width space in", field, ":", text[max(0,m.start()-10):m.end()+10])
    print("  lengths: title", len(d["title"]), "summary", len(d["summary"]), "body_md", len(d["body_md"]), "body_md_en", len(d["body_md_en"]))
