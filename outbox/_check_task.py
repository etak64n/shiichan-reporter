import json

files = [
    "aws-what-s-new-amazon-connect-customer-example-evaluations-for-agent-coaching.json",
    "aws-what-s-new-aws-glue-rest-connector-filtering-partitioning-vpc.json",
]

for f in files:
    print(f"=== {f} ===")
    d = json.load(open(f))
    print("keys:", sorted(d.keys()))
    print("body_md len:", len(d["body_md"]), "body_md_en len:", len(d["body_md_en"]))
    for k in ["title", "summary", "body_md"]:
        v = d[k]
        if "!" in v or "?" in v:
            print(f"  HALF-WIDTH !? found in {k}")
        if "<" in v:
            print(f"  RAW < found in {k}")
        for scheme in ["javascript:", "data:", "vbscript:"]:
            if scheme in v:
                print(f"  bad scheme {scheme} found in {k}")

na = json.load(open("../work/new_articles.json"))
allowed_tags = {"aws","cloudflare","openai","anthropic","microsoft","ai","ai-safety","security","infrastructure","serverless","devops","web","business","science"}
for e in na:
    d = json.load(open(e["slug"] + ".json"))
    assert d["slug"] == e["slug"]
    assert d["source_url"] == e["url"], (d["source_url"], e["url"])
    assert d["source_name"] == e["source"]
    assert d["og_title"] == e["title"], (d["og_title"], e["title"])
    assert d["published_at"] == e["published_at"]
    assert set(d["tags"]) <= allowed_tags, d["tags"]
    assert 2 <= len(d["tags"]) <= 4
    assert d["importance"] in (1,2,3,4,5)
    assert d["emotion"] in ("happy","energetic","thinking","smug","confused")
    print(e["slug"], "OK", "tags=", d["tags"], "importance=", d["importance"], "emotion=", d["emotion"])
