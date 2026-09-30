import re

with open("dashboard/index.html", "r", encoding="utf-8") as f:
    html = f.read()

scripts = re.findall(r"<script>(.*?)</script>", html, re.DOTALL)
print("Found script blocks:", len(scripts))

if scripts:
    referenced_ids = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", scripts[0])
    missing = []
    for rid in set(referenced_ids):
        if f'id="{rid}"' not in html and f"id='{rid}'" not in html:
            missing.append(rid)
    if missing:
        print("MISSING IDs in HTML:", missing)
    else:
        print(f"All {len(set(referenced_ids))} referenced element IDs exist in HTML!")
