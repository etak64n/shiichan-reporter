import json, glob

files = [
    "cloudflare-changelog-2026-08-03-python-javascript-rpc.json",
    "cloudflare-blog-grpc-workers.json",
    "cloudflare-blog-python-workers-rpc.json",
    "aws-what-s-new-amazon-ec2-i7i-instances-in-additional-regions.json",
    "aws-what-s-new-amazon-gamelift-streams.json",
]

for f in files:
    print("===", f, "===")
    d = json.load(open("outbox/" + f))
    print("keys:", sorted(d.keys()))
    print("slug:", d.get("slug"))
    print("title:", d.get("title"))
    print("title_en:", d.get("title_en"))
    print("tags:", d.get("tags"))
    print("emotion:", d.get("emotion"))
    print("importance:", d.get("importance"))
    print("source_url:", d.get("source_url"))
    print("source_name:", d.get("source_name"))
    print("og_title:", d.get("og_title"))
    print("published_at:", d.get("published_at"))
    print("body_md len:", len(d.get("body_md", "")))
    print("body_md_en len:", len(d.get("body_md_en", "")))
    print()
