import json, glob, re

REQUIRED_KEYS = ["slug","title","summary","body_md","title_en","summary_en","body_md_en","emotion","importance","source_url","source_name","og_title","tags","published_at"]
VALID_TAGS = {"aws","cloudflare","openai","anthropic","microsoft","ai","ai-safety","security","infrastructure","serverless","devops","web","business","science"]
VALID_EMOTIONS = {"happy","energetic","thinking","smug","confused"}

files = sorted(glob.glob("aws-what-s-new-*.json"))
for f in files:
    d = json.load(open(f))
    missing = [k for k in REQUIRED_KEYS if k not in d]
    problems = []
    if missing:
        problems.append(f"missing keys: {missing}")
    if d.get("emotion") not in VALID_EMOTIONS:
        problems.append(f"bad emotion: {d.get('emotion')}")
    if not isinstance(d.get("importance"), int) or not (1 <= d.get("importance",0) <= 5):
        problems.append(f"bad importance: {d.get('importance')}")
    tags = d.get("tags", [])
    bad_tags = [t for t in tags if t not in VALID_TAGS]
    if bad_tags:
        problems.append(f"invalid tags: {bad_tags}")
    if not any(t in {"aws","cloudflare","openai","anthropic","microsoft"} for t in tags):
        problems.append("no vendor tag")
    for field in ["body_md", "body_md_en"]:
        text = d.get(field, "")
        if re.search(r'<[a-zA-Z]', text):
            problems.append(f"raw HTML-like tag in {field}")
    for field in ["body_md", "title", "summary"]:
        text = d.get(field, "")
        if "!" in text or "?" in text:
            problems.append(f"half-width !/? in {field}")
    print(f, "OK" if not problems else "PROBLEMS: " + "; ".join(problems))
