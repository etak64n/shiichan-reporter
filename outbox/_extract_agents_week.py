import re, html as htmllib
html = open('outbox/_tmp_agents_week.html', encoding='utf-8').read()
html2 = re.sub(r'<script.*?</script>', '', html, flags=re.S)
html2 = re.sub(r'<style.*?</style>', '', html2, flags=re.S)
m = re.search(r'<article.*?</article>', html2, flags=re.S)
print('article found:', bool(m))
if m:
    text = m.group(0)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = htmllib.unescape(text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n', text)
    print(text[:8000])
