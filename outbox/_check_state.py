import json

files = [
 'outbox/cloudflare-changelog-2026-08-03-pipelines-billing-enabled.json',
 'outbox/cloudflare-changelog-2026-08-03-r2-sql-billing-enabled.json',
 'outbox/cloudflare-changelog-2026-08-03-r2-data-catalog-billing-enabled.json',
 'outbox/cloudflare-changelog-2026-08-04-local-tracing.json',
 'outbox/claude-code-release-v2-1-221.json',
 'outbox/cloudflare-changelog-2026-08-03-python-javascript-rpc.json',
 'outbox/cloudflare-blog-grpc-workers.json',
 'outbox/cloudflare-blog-python-workers-rpc.json',
]
for fn in files:
    d = json.load(open(fn))
    print('===', fn, '===')
    print('keys:', sorted(d.keys()))
    print('slug:', d.get('slug'))
    print('title:', d.get('title'))
    print('body_md len:', len(d.get('body_md','')))
    print('body_md_en len:', len(d.get('body_md_en','')))
    print('importance:', d.get('importance'), 'emotion:', d.get('emotion'), 'tags:', d.get('tags'))
    print()
