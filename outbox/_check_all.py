import json, glob

required = {"slug","title","summary","body_md","title_en","summary_en","body_md_en",
            "emotion","importance","source_url","source_name","og_title","tags","published_at"}

for path in sorted(glob.glob("outbox/*.json")):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        print(path, "ERROR", e)
        continue
    keys = set(d.keys())
    missing = required - keys
    extra = keys - required
    issues = []
    if missing:
        issues.append("missing " + str(missing))
    if extra:
        issues.append("extra " + str(extra))
    if not isinstance(d.get("tags"), list) or not (2 <= len(d.get("tags", [])) <= 4):
        issues.append("tags count " + str(d.get("tags")))
    if d.get("importance") not in (1,2,3,4,5):
        issues.append("importance " + str(d.get("importance")))
    if d.get("emotion") not in ("happy","energetic","thinking","smug","confused"):
        issues.append("emotion " + str(d.get("emotion")))
    if "<" in d.get("body_md","") and "&lt;" not in d.get("body_md",""):
        # crude raw-html check, ignoring markdown link angle brackets which shouldn't appear anyway
        import re
        if re.search(r"<[a-zA-Z/]", d.get("body_md","")):
            issues.append("possible raw HTML in body_md")
    print(path, "OK" if not issues else "ISSUES: " + "; ".join(issues))
