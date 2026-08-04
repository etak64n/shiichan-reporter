import json

files = [
    "outbox/cloudflare-changelog-2026-08-03-python-javascript-rpc.json",
    "outbox/cloudflare-blog-grpc-workers.json",
    "outbox/cloudflare-blog-python-workers-rpc.json",
    "outbox/cloudflare-changelog-2026-08-04-waf-release.json",
]
required = ['slug', 'title', 'summary', 'body_md', 'title_en', 'summary_en', 'body_md_en',
            'emotion', 'importance', 'source_url', 'source_name', 'og_title', 'tags', 'published_at']
valid_tags = {'aws', 'cloudflare', 'openai', 'anthropic', 'microsoft', 'ai', 'ai-safety', 'security',
              'infrastructure', 'serverless', 'devops', 'web', 'business', 'science'}
valid_emotion = {'happy', 'energetic', 'thinking', 'smug', 'confused'}

for f in files:
    d = json.load(open(f))
    missing = [k for k in required if k not in d]
    bad_tags = [t for t in d.get('tags', []) if t not in valid_tags]
    print("===", f, "===")
    print(" missing:", missing)
    print(" slug:", d.get('slug'))
    print(" emotion:", d.get('emotion'), "OK" if d.get('emotion') in valid_emotion else "BAD")
    print(" importance:", d.get('importance'))
    print(" tags:", d.get('tags'), "bad_tags:", bad_tags)
    print(" published_at:", d.get('published_at'))
    print(" title:", d.get('title'))
