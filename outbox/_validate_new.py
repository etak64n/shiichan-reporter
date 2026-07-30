import json, re

files = [
    "outbox/aws-what-s-new-amazon-connect-customer-example-evaluations-for-agent-coaching.json",
    "outbox/aws-what-s-new-aws-glue-rest-connector-filtering-partitioning-vpc.json",
]

required = ['slug','title','summary','body_md','title_en','summary_en','body_md_en',
            'emotion','importance','source_url','source_name','og_title','tags','published_at']

for f in files:
    print("==", f, "==")
    d = json.load(open(f))
    missing = [k for k in required if k not in d]
    print("missing:", missing)
    print("emotion:", d['emotion'], "importance:", d['importance'], "tags:", d['tags'])
    for k in ['body_md', 'body_md_en']:
        bad_tags = re.findall(r'<[a-zA-Z]', d[k])
        if bad_tags:
            print(k, "HTML-like tags:", bad_tags)
        for scheme in ['javascript:', 'data:', 'vbscript:']:
            if scheme in d[k]:
                print(k, "BAD SCHEME", scheme)
    if '!' in d['body_md'] or '?' in d['body_md']:
        print("body_md has half-width ! or ?")
    print("len body_md", len(d['body_md']), "len body_md_en", len(d['body_md_en']))
    print("len title", len(d['title']), "len summary", len(d['summary']))
