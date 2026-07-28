import json, re, glob

required = ['slug','title','summary','body_md','title_en','summary_en','body_md_en',
            'emotion','importance','source_url','source_name','og_title','tags','published_at']
valid_tags = {'aws','cloudflare','openai','anthropic','microsoft','ai','ai-safety','security',
              'infrastructure','serverless','devops','web','business','science'}
valid_emotions = {'happy','energetic','thinking','smug','confused'}

files = sorted(glob.glob('outbox/aws-what-s-new-*.json'))
for path in files:
    print('==', path, '==')
    d = json.load(open(path))
    missing = [k for k in required if k not in d]
    print(' missing keys:', missing)
    print(' emotion:', d['emotion'], 'valid:', d['emotion'] in valid_emotions)
    print(' importance:', d['importance'], 'valid range:', 1 <= d['importance'] <= 5)
    print(' tags:', d['tags'], 'all valid:', all(t in valid_tags for t in d['tags']))
    for field in ['body_md', 'title', 'summary', 'body_md_en', 'title_en', 'summary_en']:
        text = d[field]
        if re.search(r'<[a-zA-Z]', text):
            print(' RAW HTML SUSPECT in', field)
        if field in ('body_md','title','summary'):
            if '!' in text:
                print(' HALF WIDTH ! in', field)
            if '?' in text:
                print(' HALF WIDTH ? in', field)
        bad_links = re.findall(r'\((javascript:|data:|vbscript:)[^)]*\)', text)
        if bad_links:
            print(' BAD LINK SCHEME in', field, bad_links)
    print(' body_md len:', len(d['body_md']))
print('OK - all files parsed as valid JSON')
