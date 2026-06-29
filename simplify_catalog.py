import json
import re

def clean_name(name, brand_id):
    name = name.replace(' Kit', '').replace(' kit', '')
    name = re.sub(r' (Screen|Battery) Replacement.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r' Replacement (Screen|Battery).*', '', name, flags=re.IGNORECASE)
    name = re.sub(r' with Adhesive Strips.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r' \d+mAh.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r' -.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r' \d+G.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r' [A-Z]\d+[A-Z].*', '', name, flags=re.IGNORECASE)
    name = re.sub(r' ASSEMBLED.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r' REFURB.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r' Full Coverage.*', '', name, flags=re.IGNORECASE)
    name = name.replace('  ', ' ').strip()
    
    if brand_id == 'samsung':
        if not name.lower().startswith('galaxy'):
            if name.lower().startswith('s2') or name.lower().startswith('a5'):
                name = 'Galaxy ' + name
    
    return name

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

catalog_path = 'selfrepairkit/catalog.json'

with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

old_products = catalog['products']
new_products = {}
model_map = {} # old_id -> new_id

# 1. Create mapping and clean models
for brand in catalog['brands']:
    new_models = []
    seen_models = set()
    for m in brand['models']:
        clean = clean_name(m['name'], brand['id'])
        # Special case for "iPhone 11 to 16 Pro Max" etc - skip these ranges
        if "to" in clean.lower() and brand['id'] == 'apple': continue
        if len(clean) < 3: continue
        
        new_id = slugify(clean)
        model_map[m['id']] = new_id
        
        if new_id not in seen_models:
            new_models.append({'id': new_id, 'name': clean, 'image': m['image']})
            seen_models.add(new_id)
    brand['models'] = sorted(new_models, key=lambda x: x['name'])

# 2. Group products under new clean IDs
for old_id, items in old_products.items():
    if old_id == 'accessories':
        new_products['accessories'] = items
        continue
    
    new_id = model_map.get(old_id)
    if not new_id:
        # Try cleaning the ID directly if it wasn't in the brands list
        # (e.g. some IDs might be in products but not brands)
        new_id = slugify(clean_name(old_id.replace('-', ' '), ''))
    
    if new_id not in new_products:
        new_products[new_id] = []
    
    for item in items:
        # Standardize name for the UI
        model_name = new_id.replace('-', ' ').title()
        item['name'] = f"{model_name} {item['type']} Kit"
        new_products[new_id].append(item)

# 3. Enforce Consistency for every new model
for mid in list(new_products.keys()):
    if mid == 'accessories': continue
    items = new_products[mid]
    screens = [p for p in items if p['type'] == 'Screen']
    batteries = [p for p in items if p['type'] == 'Battery']
    
    final_items = []
    # Screens: Ensure Budget, Pro, Elite
    if screens:
        tiers = {p['tier']: p for p in screens}
        for t in ['Budget', 'Pro', 'Elite']:
            if t in tiers: final_items.append(tiers[t])
            else:
                base = screens[0]
                price = base['price']
                if t == 'Budget': price = price * 0.7
                if t == 'Elite': price = price * 1.5
                final_items.append({
                    'id': f"SRK-{mid[:5]}-{t.upper()}".upper(),
                    'name': f"{mid.replace('-', ' ').title()} Screen Kit",
                    'type': 'Screen',
                    'tier': t,
                    'price': round(price / 10) * 10 - 1,
                    'description': f"High-Performance {t} Grade"
                })
    
    # Battery: Ensure Pro
    if batteries:
        final_items.append(batteries[0])
    else:
        final_items.append({
            'id': f"SRK-{mid[:5]}-BAT".upper(),
            'name': f"{mid.replace('-', ' ').title()} Battery Kit",
            'type': 'Battery',
            'tier': 'Pro',
            'price': 59.00,
            'description': "Long-life battery cell."
        })
    new_products[mid] = final_items

catalog['products'] = new_products

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2)

print("Catalog simplification and cleaning complete.")
