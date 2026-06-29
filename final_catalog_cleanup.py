import json
import re

def is_valid_model(name, brand_id):
    name_lower = name.lower()
    # Skip accessories/tools appearing in models
    skips = ['tempered glass', 'film screen protector', 'screen protector', 'cleaning kit', 'tool', 'glue', 'adhesive']
    for skip in skips:
        if skip in name_lower: return False
    
    # Check length
    if len(name) < 3: return False
    
    # Must contain a number or series name
    if brand_id == 'apple' and 'iphone' not in name_lower: return False
    if brand_id == 'samsung' and not re.search(r'\d|fold|flip', name_lower): return False
    if brand_id == 'oppo' and not re.search(r'\d|reno|find', name_lower): return False
    
    return True

def clean_name(name, brand_id):
    # Order matters
    name = re.sub(r'(?i)REFURB (Outer|with Frame) (for|for Samsung) ', '', name)
    name = re.sub(r'(?i)Full Coverage.*for ', '', name)
    name = re.sub(r'(?i)ASSEMBLED.*for ', '', name)
    name = re.sub(r'(?i)Screen Replacement.*', '', name)
    name = re.sub(r'(?i)Replacement Battery.*', '', name)
    name = re.sub(r'(?i)Battery.*', '', name)
    name = re.sub(r'(?i)Screen.*', '', name)
    name = re.sub(r'(?i) with Adhesive.*', '', name)
    name = re.sub(r'(?i) \d+mAh.*', '', name)
    name = re.sub(r'(?i) \d+G.*', '', name)
    name = re.sub(r'(?i) [A-Z]\d+[A-Z].*', '', name)
    name = re.sub(r'(?i) Kit.*', '', name)
    name = re.sub(r' -.*', '', name)
    name = re.sub(r'(?i)Replacement.*', '', name)
    
    name = name.strip()
    
    if brand_id == 'apple':
        match = re.search(r'(?i)(iPhone \d+[\s\w]*)', name)
        if match: name = match.group(1).strip()
    elif brand_id == 'samsung':
        name = re.sub(r'(?i)Samsung ', '', name)
        if not name.lower().startswith('galaxy'):
            if re.search(r'(?i)^[SA]\d+', name) or 'fold' in name.lower() or 'flip' in name.lower():
                name = 'Galaxy ' + name
    elif brand_id == 'oppo':
        name = re.sub(r'(?i)Oppo ', '', name)
        if not name.lower().startswith('oppo'):
            name = 'OPPO ' + name

    return name.strip()

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

catalog_path = 'selfrepairkit/catalog.json'

with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

old_products = catalog['products']
new_products = {}
model_map = {}

# 1. Clean Brands/Models
for brand in catalog['brands']:
    new_models = []
    seen_models = set()
    for m in brand['models']:
        clean = clean_name(m['name'], brand['id'])
        if not is_valid_model(clean, brand['id']): continue
        
        new_id = slugify(clean)
        model_map[m['id']] = new_id
        
        if new_id not in seen_models:
            new_models.append({'id': new_id, 'name': clean, 'image': m['image']})
            seen_models.add(new_id)
    brand['models'] = sorted(new_models, key=lambda x: x['name'])

# 2. Re-group products
for old_id, items in old_products.items():
    if old_id == 'accessories':
        new_products['accessories'] = items
        continue
    
    new_id = model_map.get(old_id)
    if not new_id: continue
    
    if new_id not in new_products:
        new_products[new_id] = []
    
    for item in items:
        # Standardize name for the UI
        model_name = new_id.replace('-', ' ').title()
        item['name'] = f"{model_name} {item['type']} Kit"
        new_products[new_id].append(item)

# 3. Consolidate and fill gaps
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
                    'type': 'Screen',
                    'tier': t,
                    'price': round(price / 10) * 10 - 1,
                    'description': f"High-Performance {LABELS[t]} Grade"
                })
    if batteries: final_items.append(batteries[0])
    else: final_items.append({'id': f"SRK-{mid[:5]}-BAT".upper(), 'name': f"{mid.replace('-',' ').title()} Battery Kit", 'type': 'Battery', 'tier': 'Pro', 'price': 59.00, 'description': "Long-life battery cell."})
    new_products[mid] = final_items

catalog['products'] = new_products

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2)

print("Catalog final cleanup complete.")
