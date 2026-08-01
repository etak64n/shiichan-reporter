import json, glob

for f in sorted(glob.glob("outbox/*.json")):
    if "/_" in f or f.endswith("_task5.py"):
        continue
    d = json.load(open(f))
    print("===", f, "===")
    for k in ["slug","title","emotion","importance","source_url","source_name","og_title","tags","published_at"]:
        print(k, ":", d.get(k))
    print("body_md len:", len(d.get("body_md","")))
    print("body_md_en len:", len(d.get("body_md_en","")))
    print("title_en:", d.get("title_en"))
    print("summary:", d.get("summary"))
    print("summary_en:", d.get("summary_en"))
    print()
