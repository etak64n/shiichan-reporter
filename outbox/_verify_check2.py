import json, re, glob
for f in sorted(glob.glob('outbox/*.json')):
    if f.split('/')[-1].startswith('_'):
        continue
    d = json.load(open(f))
    print('===', f)
    for k in ['body_md','body_md_en','title','summary']:
        v = d.get(k,'')
        bad = re.findall(r'[!?]', v) if k in ('body_md','title','summary') else []
        if bad:
            print(' half-width !? found in', k, len(bad))
    for k in ['body_md','body_md_en']:
        v = d.get(k,'')
        htmltags = re.findall(r'<[a-zA-Z]', v)
        if htmltags:
            print(' HTML-ish tag found in', k, htmltags[:5])
    for k in ['body_md','body_md_en']:
        v = d.get(k,'')
        if re.search(r'(javascript:|data:|vbscript:)', v):
            print(' suspicious scheme in', k)
    print(' title:', d.get('title'))
    print(' importance:', d.get('importance'), 'emotion:', d.get('emotion'), 'tags:', d.get('tags'))
    print(' body_md len:', len(d.get('body_md','')), 'body_md_en len:', len(d.get('body_md_en','')))
    print(' published_at:', d.get('published_at'))
    print(' keys:', sorted(d.keys()))
