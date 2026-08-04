import json, re

with open("work/new_articles.json") as f:
    new_articles = json.load(f)
slugs = [a["slug"] for a in new_articles]

required = ["slug","title","summary","body_md","title_en","summary_en","body_md_en","emotion","importance","source_url","source_name","og_title","tags","published_at"]
valid_tags_vendor = {"aws","cloudflare","openai","anthropic","microsoft"}
valid_tags_cat = {"ai","ai-safety","security","infrastructure","serverless","devops","web","business","science"}
valid_emotion = {"happy","energetic","thinking","smug","confused"}

problems = []
missing = []
for slug in slugs:
    path = "outbox/" + slug + ".json"
    try:
        d = json.load(open(path))
    except FileNotFoundError:
        missing.append(slug)
        continue
    for k in required:
        if k not in d:
            problems.append((slug, "missing key " + k))
    if d.get("slug") != slug:
        problems.append((slug, "slug mismatch"))
    if d.get("emotion") not in valid_emotion:
        problems.append((slug, "bad emotion " + str(d.get("emotion"))))
    imp = d.get("importance")
    if not isinstance(imp, int) or not (1 <= imp <= 5):
        problems.append((slug, "bad importance " + str(imp)))
    tags = d.get("tags", [])
    if not (2 <= len(tags) <= 4):
        problems.append((slug, "tag count " + str(len(tags))))
    vend = [t for t in tags if t in valid_tags_vendor]
    if len(vend) != 1:
        problems.append((slug, "vendor tag count " + str(vend)))
    bad_tags = [t for t in tags if t not in valid_tags_vendor and t not in valid_tags_cat]
    if bad_tags:
        problems.append((slug, "unknown tags " + str(bad_tags)))
    for field in ["body_md","body_md_en","title","summary","summary_en","title_en"]:
        val = d.get(field,"")
        if re.search(r"<[a-zA-Z]", val):
            problems.append((slug, "raw HTML-looking tag in " + field))
    for field in ["body_md","body_md_en"]:
        val = d.get(field,"")
        for m in re.finditer(r"\]\(([^)]+)\)", val):
            url = m.group(1)
            if not (url.startswith("http://") or url.startswith("https://")):
                problems.append((slug, "bad link scheme in " + field + ": " + url))

print("Missing:", missing)
print("Problems:")
for p in problems:
    print(" ", p)
print("Total slugs checked:", len(slugs))
