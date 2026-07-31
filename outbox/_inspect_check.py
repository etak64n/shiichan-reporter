import json

files = [
 'cloudflare-changelog-2026-07-24-r2-sippy-azure-s3-compatible-support.json',
 'aws-what-s-new-aws-msk-streaming-tables-for-apache-iceberg.json',
 'cloudflare-changelog-2026-07-30-rotate-stream-broadcast-keys.json',
 'cloudflare-changelog-2026-07-31-wrangler-startup-profile-summary.json',
 'openai-news-unive.json',
]
for f in files:
    d = json.load(open(f))
    print("===", f)
    print("keys:", sorted(d.keys()))
    for k in ['slug','title','title_en','emotion','importance','source_url','source_name','og_title','tags','published_at']:
        print(" ", k, "=", d.get(k))
    print("  body_md len:", len(d.get('body_md','')), "body_md_en len:", len(d.get('body_md_en','')))
    print("  summary:", d.get('summary','')[:120])
