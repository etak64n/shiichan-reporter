import json, os

files = [
    "cloudflare-changelog-2026-07-24-r2-sippy-azure-s3-compatible-support",
    "aws-what-s-new-aws-msk-streaming-tables-for-apache-iceberg",
    "cloudflare-changelog-2026-07-30-rotate-stream-broadcast-keys",
    "aws-what-s-new-aws-codedeploy-five-additional-regions",
    "cloudflare-blog-moq-relays",
]

for f in files:
    path = os.path.join("outbox", f + ".json")
    print("---", f, "---")
    if os.path.exists(path):
        d = json.load(open(path))
        print("slug:", d.get("slug"))
        print("title:", d.get("title"))
        print("len body_md:", len(d.get("body_md", "")))
        print("keys:", sorted(d.keys()))
    else:
        print("MISSING")
