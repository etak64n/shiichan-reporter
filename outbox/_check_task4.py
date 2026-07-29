import json, re

with open('outbox/openai-news-how-two-settings-tripled-our-arc-agi-3-scores.json', encoding='utf-8') as f:
    d = json.load(f)

print('OK, keys:', list(d.keys()))
print('body_md len:', len(d['body_md']))
print('body_md_en len:', len(d['body_md_en']))
print('title len:', len(d['title']))
print('summary len:', len(d['summary']))

for k in ['title', 'summary', 'body_md']:
    if '!' in d[k] or '?' in d[k]:
        print('WARNING half-width punctuation in', k)

for k in ['body_md', 'body_md_en']:
    if re.search(r'<[a-zA-Z]', d[k]):
        print('WARNING html-like tag in', k)

print('tags:', d['tags'])
print('emotion:', d['emotion'], 'importance:', d['importance'])
print('slug:', d['slug'])
print('source_url:', d['source_url'])
print('published_at:', d['published_at'])
