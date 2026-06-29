import json

PATH = "selfrepairkit/groups.json"
SAMSUNG_CP = {"galaxy-a-series": 79, "galaxy-s-series-s21-s26": 99}

data = json.load(open(PATH, encoding="utf-8"))
changed = []
for g in data["groups"]:
    if g.get("brand") != "samsung":
        continue
    price = SAMSUNG_CP.get(g["id"])
    if price is None:                      # fallback if an id ever changes
        n = g.get("name", "").lower()
        if "a-series" in n or "a series" in n: price = 79
        elif "s-series" in n or "s2" in n:     price = 99
    if price is None:
        continue
    g["repairs"].pop("charging port", None)            # remove old space-key
    g["repairs"]["charging_port"] = {m: {"standard": price} for m in g["models"]}
    changed.append(f'{g["id"]}: ${price} x {len(g["models"])} models')

json.dump(data, open(PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("charging_port updated for:")
for c in changed: print("  -", c)
