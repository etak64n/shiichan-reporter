import json, glob, re

allowed_tags = {"aws","cloudflare","openai","anthropic","microsoft",
    "ai","ai-safety","security","infrastructure","serverless","devops","web","business","science"}
vendor_tags = {"aws","cloudflare","openai","anthropic","microsoft"}
allowed_emotion = {"happy","energetic","thinking","smug","confused"}

new_articles = json.load(open("work/new_articles.json"))
slugs = {a["slug"]: a for a in new_articles}

files = [f for f in glob.glob("outbox/*.json") if not f.split("/")[-1].startswith("_")]
print("Files:", files)

for f in sorted(files):
    d = json.load(open(f))
    slug = d.get("slug")
    fname = f.split("/")[-1][:-5]
    problems = []
    if slug != fname:
        problems.append("slug/filename mismatch: %s vs %s" % (slug, fname))
    if slug in slugs:
        src = slugs[slug]
        if d.get("source_url") != src["url"]:
            problems.append("source_url mismatch")
        if d.get("source_name") != src["source"]:
            problems.append("source_name mismatch")
        pub = src.get("published_at")
        if pub is not None and d.get("published_at") != pub:
            problems.append("published_at mismatch: %s vs %s" % (d.get("published_at"), pub))
    else:
        problems.append("slug not found in new_articles.json")
    for k in ["title","summary","body_md","title_en","summary_en","body_md_en","emotion","importance","source_url","source_name","og_title","tags","published_at"]:
        if k not in d:
            problems.append("missing field %s" % k)
    if d.get("emotion") not in allowed_emotion:
        problems.append("bad emotion %s" % d.get("emotion"))
    imp = d.get("importance")
    if not isinstance(imp,int) or not (1<=imp<=5):
        problems.append("bad importance %s" % imp)
    tags = d.get("tags",[])
    if not (2<=len(tags)<=4):
        problems.append("tag count %d" % len(tags))
    if not any(t in vendor_tags for t in tags):
        problems.append("no vendor tag")
    for t in tags:
        if t not in allowed_tags:
            problems.append("tag not in allowed list: %s" % t)
    for field in ["body_md","body_md_en"]:
        text = d.get(field,"")
        if re.search(r'<[a-zA-Z/]', text):
            problems.append("raw HTML-like tag in %s" % field)
        for m in re.finditer(r'\]\(([^)]+)\)', text):
            url = m.group(1)
            if not (url.startswith("http://") or url.startswith("https://")):
                problems.append("bad link scheme in %s: %s" % (field, url))
    if len(d.get("title","")) > 300: problems.append("title too long")
    if len(d.get("summary","")) > 1000: problems.append("summary too long")
    if len(d.get("body_md","").encode('utf-8')) > 65536: problems.append("body_md too long")
    if len(d.get("title_en","")) > 300: problems.append("title_en too long")
    if len(d.get("summary_en","")) > 1000: problems.append("summary_en too long")
    if len(d.get("body_md_en","").encode('utf-8')) > 65536: problems.append("body_md_en too long")

    status = "OK" if not problems else "PROBLEMS: " + "; ".join(problems)
    print("%s: %s" % (fname, status))
