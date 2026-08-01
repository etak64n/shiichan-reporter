import json, glob, os
for f in sorted(glob.glob('outbox/*.json')):
    if os.path.basename(f) == '_permtest.json':
        continue
    try:
        d = json.load(open(f))
        print(f, 'OK', 'slug=' + str(d.get('slug')), 'keys=' + str(sorted(d.keys())))
    except Exception as e:
        print(f, 'FAIL', e)
