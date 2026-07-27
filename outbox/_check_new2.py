import json, re

files = [
    "outbox/anthropic-news-cognizant-anthropic.json",
    "outbox/aws-blog-aws-weekly-roundup-july-27-2026.json",
    "outbox/cloudflare-blog-open-sourcing-our-privacy-proxy-cli.json",
    "outbox/cloudflare-changelog-2026-07-21-integration-test-harness.json",
]

required_keys = {"slug","title","summary","body_md","title_en","summary_en","body_md_en",
                  "emotion","importance","source_url","source_name","og_title","tags","published_at"}
valid_tags = {"aws","cloudflare","openai","anthropic","microsoft",
              "ai","ai-safety","security","infrastructure","serverless","devops","web","business","science"}
valid_emotions = {"happy","energetic","thinking","smug","confused"}

for f in files:
    d = json.load(open(f))
    print("===", f, "===")
    missing = required_keys - set(d.keys())
    if missing: print("MISSING KEYS:", missing)
    if len(d["title"]) > 300: print("title too long")
    if len(d["summary"]) > 1000: print("summary too long")
    if len(d["body_md"].encode()) > 65536: print("body_md too long")
    if len(d["title_en"]) > 300: print("title_en too long")
    if len(d["summary_en"]) > 1000: print("summary_en too long")
    if len(d["body_md_en"].encode()) > 65536: print("body_md_en too long")
    if d["emotion"] not in valid_emotions: print("bad emotion:", d["emotion"])
    if not (1 <= d["importance"] <= 5): print("bad importance:", d["importance"])
    if not isinstance(d["importance"], int): print("importance not int")
    bad_tags = set(d["tags"]) - valid_tags
    if bad_tags: print("BAD TAGS:", bad_tags)
    vendor_tags = {"aws","cloudflare","openai","anthropic","microsoft"} & set(d["tags"])
    if len(vendor_tags) != 1: print("vendor tag count issue:", vendor_tags)
    if not (2 <= len(d["tags"]) <= 4): print("tag count issue:", len(d["tags"]))
    for field in ["title","summary","body_md"]:
        text = d[field]
        if "!" in text or "?" in text:
            print("half-width bang/question found in", field)
    if re.search(r'<[a-zA-Z]', d["body_md"]):
        print("raw HTML tag suspected in body_md")
    if re.search(r'<[a-zA-Z]', d["body_md_en"]):
        print("raw HTML tag suspected in body_md_en")
    if re.search(r'(javascript|data|vbscript):', d["body_md"], re.I):
        print("suspicious scheme in body_md")
    print("OK checked. title:", d["title"][:50])
