import json
import re

def slugify(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def is_requested_model(name, brand_id):
    name = name.lower()
    if brand_id == 'apple':
        if 'iphone' not in name: return False
        match = re.search(r'iphone\s+(\d+|se|x[rs]?)', name)
        if match:
            val = match.group(1)
            if val in ['se', 'x', 'xr', 'xs']: return True
            try:
                num = int(val)
                return 7 <= num <= 18
            except: return False
        return False
    if brand_id == 'samsung':
        if any(x in name for x in ['tab', 'note', 'fold', 'flip', 'watch', 'book', 'buds']): return False
        if "galaxy s" in name or "galaxy a" in name: return True
        if re.search(r'^[sa]\d+', name): return True
        return False
    return brand_id == 'oppo'

catalog_path = 'selfrepairkit/catalog.json'
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

old_products = catalog['products']
allowed_ids = set()

for brand in catalog['brands']:
    bid = brand['id']
    clean_models = []
    seen = set()
    
    # 1. Collect all current models regardless of previous grouping
    current_models = []
    if 'models' in brand: current_models = brand['models']
    elif 'groups' in brand:
        for g in brand['groups']: current_models.extend(g['models'])

    for m in current_models:
        if is_requested_model(m['name'], bid):
            mid = slugify(m['name'])
            if mid not in seen:
                clean_models.append(m)
                seen.add(mid)
                allowed_ids.add(mid)
    
    # 2. Add missing S-series (S22-S26)
    if bid == 'samsung':
        for s in ['S22', 'S23', 'S24', 'S25', 'S26']:
            for v in ['', ' Plus', ' Ultra', ' FE']:
                name = f"Galaxy {s}{v}"
                mid = slugify(name)
                if mid not in seen:
                    clean_models.append({"id": mid, "name": name, "image": "https://sc02.alicdn.com/kf/Ac8c64183dc2a4b9894fa022cce6d4611U.png"})
                    seen.add(mid); allowed_ids.add(mid)
                    
    # 3. Add missing iPhone series (7-18)
    if bid == 'apple':
        for n in range(7, 19):
            for v in ['', ' Plus', ' Pro', ' Pro Max', ' mini']:
                if n < 11 and (v == ' Pro' or v == ' Pro Max'): continue
                if n > 8 and v == ' Plus' and n < 14: continue
                name = f"iPhone {n}{v}"
                mid = slugify(name)
                if mid not in seen:
                    clean_models.append({"id": mid, "name": name, "image": "https://sc02.alicdn.com/kf/Ac8c64183dc2a4b9894fa022cce6d4611U.png"})
                    seen.add(mid); allowed_ids.add(mid)

    brand['models'] = sorted(clean_models, key=lambda x: x['name'])
    if 'groups' in brand: del brand['groups'] # Reset for regrouping

# 4. Filter and fill products
new_products = {}
LABELS = { 'Budget': 'Aftermarket Incell', 'Pro': 'Aftermarket OLED', 'Elite': 'OEM Original' }
for mid in allowed_ids:
    items = old_products.get(mid, [])
    screens = [p for p in items if p.get('type') == 'Screen']
    batteries = [p for p in items if p.get('type') == 'Battery']
    final_items = []
    
    tiers = {p['tier']: p for p in screens}
    base_price = 189.0 if not screens else screens[0]['price']
    for t in ['Budget', 'Pro', 'Elite']:
        if t in tiers: final_items.append(tiers[t])
        else:
            p = base_price
            if t == 'Budget': p = base_price * 0.6
            if t == 'Elite': p = base_price * 1.4
            if '18' in mid or 's26' in mid: p += 100
            final_items.append({
                'id': f"SRK-{mid[:5]}-{t.upper()}".upper(), 'name': f"{mid.replace('-',' ').title()} Screen Kit",
                'type': 'Screen', 'tier': t, 'price': round(p / 10) * 10 - 1,
                'description': f"Professional {LABELS[t]} Grade"
            })
    if batteries: final_items.append(batteries[0])
    else: final_items.append({'id': f"SRK-{mid[:5]}-BAT".upper(), 'name': f"{mid.replace('-',' ').title()} Battery Kit", 'type': 'Battery', 'tier': 'Pro', 'price': 69.00, 'description': "Long-life cell."})
    new_products[mid] = final_items

new_products['accessories'] = old_products.get('accessories', [])
catalog['products'] = new_products

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2)

print("Exhaustive clean of requested series complete. Z/Note/Tabs removed.")
