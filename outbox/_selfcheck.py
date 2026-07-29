import json, re

slugs = [
 "cloudflare-changelog-2026-07-27-audit-logs-v2-resource-history",
 "openai-news-gpt-5-6-frontier-intelligence-efficiency",
 "aws-what-s-new-aws-waf",
 "openai-news-how-two-settings-tripled-our-arc-agi-3-scores",
 "aws-what-s-new-amazon-redshift-data-api-longpolling-listsession-flexiblebatchexecute",
 "aws-what-s-new-ec2-auto-scaling-instance-refresh-cloudformation",
]

required = ["slug","title","summary","body_md","title_en","summary_en","body_md_en","emotion","importance","source_url","source_name","og_title","tags","published_at"]
valid_tags = {"aws","cloudflare","openai","anthropic","microsoft","ai","ai-safety","security","infrastructure","serverless","devops","web","business","science"}
vendors = {"aws","cloudflare","openai","anthropic","microsoft"}
valid_emotion = {"happy","energetic","thinking","smug","confused"}

for slug in slugs:
    path = "outbox/" + slug + ".json"
    print("====", path)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("  ERROR loading:", e)
        continue
    missing = [k for k in required if k not in data]
    if missing: print("  MISSING FIELDS:", missing)
    if data.get("slug") != slug: print("  SLUG MISMATCH:", data.get("slug"))
    for k in ["title","summary","title_en","summary_en"]:
        limit = 1000 if "summary" in k else 300
        if len(data.get(k,"")) > limit:
            print("  " + k + " too long: " + str(len(data[k])))
    for k in ["body_md","body_md_en"]:
        n = len(data.get(k,"").encode("utf-8"))
        if n > 65536: print("  " + k + " too large bytes: " + str(n))
    if data.get("emotion") not in valid_emotion: print("  BAD EMOTION:", data.get("emotion"))
    imp = data.get("importance")
    if not isinstance(imp,int) or not (1<=imp<=5): print("  BAD IMPORTANCE:", imp)
    tags = data.get("tags",[])
    if not (2<=len(tags)<=4): print("  BAD TAG COUNT:", tags)
    bad_tags = [t for t in tags if t not in valid_tags]
    if bad_tags: print("  UNKNOWN TAGS:", bad_tags)
    if not any(t in vendors for t in tags): print("  NO VENDOR TAG:", tags)
    body = data.get("body_md","")
    html_hits = re.findall(r'<[a-zA-Z]', body)
    if html_hits: print("  POSSIBLE RAW HTML in body_md:", html_hits[:5])
    body_en = data.get("body_md_en","")
    html_hits_en = re.findall(r'<[a-zA-Z]', body_en)
    if html_hits_en: print("  POSSIBLE RAW HTML in body_md_en:", html_hits_en[:5])
    half = re.findall(r'[!?]', body)
    if half: print("  HALF-WIDTH !/? COUNT in body_md:", len(half))
    bad_links = re.findall(r'\]\((?!https?://)[^)]+\)', body)
    if bad_links: print("  NON-HTTP(S) LINK in body_md:", bad_links[:5])
    for phrase in ["試してみた","使ってみた","試した結果"]:
        if phrase in body:
            print("  EXPERIENTIAL PHRASE found: " + phrase)
    print("  OK title:", data.get("title"))
    print("  tags:", tags, "emotion:", data.get("emotion"), "importance:", imp)
    print("  published_at:", data.get("published_at"), "source_url:", data.get("source_url"))
