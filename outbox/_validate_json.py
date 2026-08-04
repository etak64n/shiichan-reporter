import json
import sys

for path in sys.argv[1:]:
    try:
        json.load(open(path))
        print(path, "VALID")
    except Exception as e:
        print(path, "INVALID:", e)
