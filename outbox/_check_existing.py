import json, glob

for f in sorted(glob.glob("outbox/aws-what-s-new-*.json")):
    d = json.load(open(f))
    print("==", f, "==")
    print("slug:", d.get("slug"))
    print("title:", d.get("title"))
    print("body_md len:", len(d.get("body_md", "")))
    print("body_md_en len:", len(d.get("body_md_en", "")))
    print("tags:", d.get("tags"))
    print("importance:", d.get("importance"))
    print("emotion:", d.get("emotion"))
    print("published_at:", d.get("published_at"))
    print("source_url:", d.get("source_url"))
    print()
