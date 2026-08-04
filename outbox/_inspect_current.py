import json
files = [
"outbox/aws-what-s-new-amazon-bedrock-web.json",
"outbox/aws-what-s-new-amazon-ec2-c8g-instances-additional-regions.json",
"outbox/aws-what-s-new-amazon-emr-ec2-spark-connect.json",
"outbox/aws-what-s-new-aws-application-network.json",
"outbox/aws-what-s-new-aws-security-hub-extended-adds-supply-chain-security.json",
"outbox/aws-what-s-new-rds-sql-server-supports-developer-edition-in-additional-aws-regions.json",
"outbox/cloudflare-blog-grpc-workers.json",
"outbox/cloudflare-blog-python-workers-rpc.json",
"outbox/cloudflare-changelog-2026-08-03-python-javascript-rpc.json",
"outbox/cloudflare-changelog-2026-08-04-free-dashboard-button.json",
"outbox/openai-news-third-party-cyber-evaluations-involving-openai-models.json",
]
for f in files:
    try:
        d = json.load(open(f))
    except Exception as e:
        print(f, "ERROR", e)
        continue
    print("==", f)
    print(" keys:", sorted(d.keys()))
    print(" slug:", d.get("slug"))
    print(" title:", d.get("title"))
    print(" body_md len:", len(d.get("body_md","")), "body_md_en len:", len(d.get("body_md_en","")))
    print(" tags:", d.get("tags"), "importance:", d.get("importance"), "emotion:", d.get("emotion"))
    print(" source_url:", d.get("source_url"))
    print(" published_at:", d.get("published_at"))
