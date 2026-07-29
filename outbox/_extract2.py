import re
html = open('outbox/_waf_raw.html', encoding='utf-8', errors='ignore').read()
html = re.sub(r'<script.*?</script>', '', html, flags=re.S)
html = re.sub(r'<style.*?</style>', '', html, flags=re.S)
text = re.sub(r'<[^>]+>', '\n', html)
text = re.sub(r'\n\s*\n+', '\n', text)
open('outbox/_waf_text.txt', 'w', encoding='utf-8').write(text)
print(len(text))
