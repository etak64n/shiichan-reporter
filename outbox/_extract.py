import re
html = open('/home/runner/work/shiichan-reporter/shiichan-reporter/outbox/_cf.html', encoding='utf-8').read()
html = re.sub(r'<script.*?</script>', '', html, flags=re.S)
html = re.sub(r'<style.*?</style>', '', html, flags=re.S)
text = re.sub(r'<[^>]+>', '\n', html)
text = re.sub(r'\n\s*\n+', '\n', text)
lines = [l.strip() for l in text.split('\n') if l.strip()]
open('/home/runner/work/shiichan-reporter/shiichan-reporter/outbox/_cf.txt','w').write('\n'.join(lines))
print(len(lines))
