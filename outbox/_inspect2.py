import json, glob

for f in sorted(glob.glob('outbox/aws-*.json')):
    d = json.load(open(f))
    print('===', f, '===')
    print('keys:', sorted(d.keys()))
    print('slug:', d.get('slug'))
    print('title:', d.get('title'))
    print('title_en:', d.get('title_en'))
    print('tags:', d.get('tags'))
    print('emotion:', d.get('emotion'))
    print('importance:', d.get('importance'))
    print('published_at:', d.get('published_at'))
    print('source_url:', d.get('source_url'))
    print('source_name:', d.get('source_name'))
    print('og_title:', d.get('og_title'))
    print('body_md len:', len(d.get('body_md', '')))
    print('body_md_en len:', len(d.get('body_md_en', '')))
    print()
