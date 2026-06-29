import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def clean_model_name(name, brand_id):
    original = name
    # Strip marketing brands and quality descriptors
    junk = [
        r'(?i)GREENCELL\s+', r'(?i)KINGLAS\s+', r'(?i)REPAIRRANGE\s+', r'(?i)AMPLUS\s+',
        r'(?i)REFURB\s+', r'(?i)AS\s+NEW\s+', r'(?i)FULL\s+COVERAGE\s*', r'(?i)TEMPERED\s+GLASS\s*',
        r'(?i)SHIELD\s*', r'(?i)PRO\d+\s*', r'(?i)DIAGNOSABLE\s*', r'(?i)ASSEMBLY\s*',
        r'(?i)SCREEN\s+REPLACEMENT\s*', r'(?i)BATTERY\s+REPLACEMENT\s*'
    ]
    for pattern in junk:
        name = re.sub(pattern, '', name)
    
    name = name.strip()
    
    # Normalize Samsung
    if brand_id == 'samsung':
        name = re.sub(r'(?i)Galaxy\s+', '', name)
        name = re.sub(r'(?i)Samsung\s+', '', name)
        # Handle core S/A/Note/Z series
        if re.search(r'(?i)^[SAZ]\d+|Note|Fold|Flip', name):
            # Ensure no stray technical codes like G998B
            name = re.sub(r'\s+[A-Z]\d+.*', '', name)
            return "Galaxy " + name.strip()
        return None # Filter out non-matching junk
        
    # Normalize iPhone
    if brand_id == 'apple':
        name = re.sub(r'(?i)iPhone\s+', '', name)
        if re.search(r'^\d+|SE|X[RS]?', name):
            return "iPhone " + name.strip()
        return None

    # Normalize OPPO
    if brand_id == 'oppo':
        name = re.sub(r'(?i)OPPO\s+', '', name)
        if re.search(r'^[A-Z0-9]+|Reno|Find', name):
            return "OPPO " + name.strip()
        return None

    return name if len(name) > 2 else None

catalog_path = 'selfrepairkit/catalog.json'

with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

old_products = catalog['products']
new_products = {}
model_map = {} # old_id -> new_id

# 1. Clean Models in Brands
for brand in catalog['brands']:
    clean_models = []
    seen = set()
    for m in brand['models']:
        c_name = clean_model_name(m['name'], brand['id'])
        if not c_name: continue
        
        # Consolidation check: "Greencell S25" -> "Galaxy S25"
        new_id = slugify(c_name)
        model_map[m['id']] = new_id
        
        if new_id not in seen:
            clean_models.append({'id': new_id, 'name': c_name, 'image': m['image']})
            seen.add(new_id)
            
    brand['models'] = sorted(clean_models, key=lambda x: x['name'])

# 2. Merge Products under Clean IDs
for old_id, items in old_products.items():
    if old_id == 'accessories':
        new_products['accessories'] = items
        continue
    
    new_id = model_map.get(old_id)
    if not new_id: continue # Filter out junk that didn't map
    
    if new_id not in new_products:
        new_products[new_id] = []
    
    # Merge existing items, avoiding duplicates
    existing_ids = {p['id'] for p in new_products[new_id]}
    for item in items:
        if item['id'] not in existing_ids:
            # Standardize internal product names for UI clarity
            model_name = new_id.replace('-', ' ').title()
            item['name'] = f"{model_name} {item['type']} Kit"
            new_products[new_id].append(item)
            existing_ids.add(item['id'])

# 3. Final Consistency pass (ensuring 3 tiers + battery for every model)
LABELS = { 'Budget': 'Aftermarket Incell', 'Pro': 'Aftermarket OLED', 'Elite': 'OEM Original' }
for mid in list(new_products.keys()):
    if mid == 'accessories': continue
    items = new_products[mid]
    screens = [p for p in items if p['type'] == 'Screen']
    batteries = [p for p in items if p['type'] == 'Battery']
    
    final_items = []
    if screens:
        screens = sorted(screens, key=lambda x: x['price'])
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
                    'type': 'Screen', 'tier': t, 'price': round(price / 10) * 10 - 1, 
                    'description': f"High-Performance {LABELS[t]} Grade"
                })
    if batteries: final_items.append(batteries[0])
    else: final_items.append({'id': f"SRK-{mid[:5]}-BAT".upper(), 'name': f"{mid.replace('-',' ').title()} Battery Kit", 'type': 'Battery', 'tier': 'Pro', 'price': 59.00, 'description': "Long-life cell."})
    new_products[mid] = final_items

catalog['products'] = new_products

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2)

print("Strict catalog cleanup complete. Junk entries removed.")
