import json, re

files = [
 'outbox/aws-what-s-new-kiro-opus-sonnet-monitoring-launch-aws-govcloud-us.json',
 'outbox/aws-what-s-new-aws-lambda-managed-instances-logs.json',
 'outbox/aws-what-s-new-on-demand-scale-down.json',
 'outbox/aws-what-s-new-ec2-dedicated-hosts-hrg.json',
]
required = ['slug','title','summary','body_md','title_en','summary_en','body_md_en','emotion','importance','source_url','source_name','og_title','tags','published_at']
for f in files:
    d = json.load(open(f))
    missing = [k for k in required if k not in d]
    issues = []
    if missing: issues.append('missing:'+str(missing))
    for field in ['body_md','title','summary']:
        v = d[field]
        if re.search(r'[!?]', v): issues.append(field + ': halfwidth !/?')
        if re.search(r'<[a-zA-Z]', v): issues.append(field + ': raw HTML tag')
    if not (2 <= len(d['tags']) <= 4): issues.append('tags count')
    if not (1 <= d['importance'] <= 5): issues.append('importance range')
    print(f, 'OK' if not issues else issues)
