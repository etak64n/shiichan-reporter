import re
html = open('outbox/_anthropic_raw.html', encoding='utf-8').read()
html = re.sub(r'<script[\s\S]*?</script>', '', html)
html = re.sub(r'<style[\s\S]*?</style>', '', html)
text = re.sub(r'<[^>]+>', '\n', html)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'&#x27;|&#39;', "'", text)
text = re.sub(r'&quot;', '"', text)
text = re.sub(r'\n\s*\n+', '\n\n', text)
lines = [l.strip() for l in text.split('\n') if l.strip()]
with open('outbox/_anthropic_lines.txt', 'w') as f:
    f.write('\n'.join(lines))
print(len(lines))
