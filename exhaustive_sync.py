import csv
import json
import re

def clean_model_name(text, brand):
    # Common patterns to remove
    removals = [
        r'Assembly for', r'Screen Replacement', r'Battery Replacement',
        r'OLED', r'LCD', r'Incell', r'Diagnosable', r'Compatible.*', 
        r'\(.*\)', r'Assembly', r'Replacement', r'Premium', r'Genuine',
        r'Aftermarket', r'Kit', r'Hard', r'Soft', r'Module'
    ]
    
    # Handle Samsung specifically
    if brand == "Samsung":
        # Extract Galaxy S/A/Note series
        match = re.search(r'(Galaxy [S|A|Note|Fold|Flip]\d+[\+]?[\s\w]*)', text, re.IGNORECASE)
        if match: return match.group(1).strip()
    
    # Handle iPhone specifically
    if brand == "Apple":
        match = re.search(r'(iPhone \d+[\s\w]*)', text, re.IGNORECASE)
        if match: return match.group(1).strip()
        
    # Handle OPPO
    if brand == "OPPO":
        match = re.search(r'(OPPO [A-Z0-9]+[\s\w]*)', text, re.IGNORECASE)
        if match: return match.group(1).strip()
        # Fallback for Reno/Find
        match = re.search(r'(Reno \d+[\s\w]*|Find X\d+[\s\w]*)', text, re.IGNORECASE)
        if match: return match.group(1).strip()

    name = text
    for p in removals:
        name = re.sub(p, '', name, flags=re.IGNORECASE)
    
    return name.strip()

def calculate_price(cost):
    try:
        c = float(cost)
        price = (c + 39) * 1.4
        rounded = round(price / 10) * 10 - 1
        return float(rounded)
    except:
        return 0.0

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def map_tier(raw_tier, text):
    raw = (raw_tier + " " + text).lower()
    if "incell" in raw or "lcd" in raw or "budget" in raw: return "Budget"
    if "original" in raw or "oem" in raw or "service pack" in raw or "pull" in raw or "elite" in raw: return "Elite"
    return "Pro"

costs_path = 'RR project/leads/crazyparts_exhaustive_costs.csv'
catalog_path = 'selfrepairkit/catalog.json'

brands_data = {
    'Apple': {'id': 'apple', 'name': 'iPhone Kit', 'icon': 'smartphone', 'models': {}},
    'Samsung': {'id': 'samsung', 'name': 'Samsung Kit', 'icon': 'tablet', 'models': {}},
    'OPPO': {'id': 'oppo', 'name': 'OPPO Kit', 'icon': 'activity', 'models': {}}
}

products_data = {}

with open(costs_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        brand = row['Brand']
        full_text = row['Full Model Name']
        part_type = row['Part Type']
        tier_raw = row['Quality/Tier']
        cost = row['Diamond Price']
        
        if brand not in brands_data: continue
        
        model_name = clean_model_name(full_text, brand)
        if not model_name: continue
        
        # Split grouped models
        individual_models = [m.strip() for m in model_name.split('/')]
        
        for m_name in individual_models:
            mid = slugify(m_name)
            
            if mid not in brands_data[brand]['models']:
                brands_data[brand]['models'][mid] = {
                    'id': mid,
                    'name': m_name,
                    'image': 'https://sc02.alicdn.com/kf/Ac8c64183dc2a4b9894fa022cce6d4611U.png'
                }
            
            if mid not in products_data: products_data[mid] = []
            
            products_data[mid].append({
                'id': f"SRK-{mid[:5]}-{slugify(tier_raw)[:10]}".upper(),
                'name': f"{m_name} {part_type} Kit",
                'type': part_type,
                'tier': map_tier(tier_raw, full_text),
                'price': calculate_price(cost),
                'description': f"Premium {tier_raw} replacement part."
            })

# Finalize structure
final_brands = []
for b in brands_data.values():
    b_copy = b.copy()
    b_copy['models'] = sorted(list(b['models'].values()), key=lambda x: x['name'])
    final_brands.append(b_copy)

# Preserve extras
with open(catalog_path, 'r', encoding='utf-8') as f:
    old = json.load(f)
    products_data['accessories'] = old['products'].get('accessories', [])

# Consistency Check
for mid, items in products_data.items():
    if mid == 'accessories': continue
    screens = [p for p in items if p['type'] == 'Screen']
    batteries = [p for p in items if p['type'] == 'Battery']
    
    final_items = []
    if screens:
        tiers = {p['tier']: p for p in screens}
        for t in ['Budget', 'Pro', 'Elite']:
            if t in tiers: final_items.append(tiers[t])
            else:
                base = screens[0]
                p = base['price']
                if t == 'Budget': p = p * 0.7
                if t == 'Elite': p = p * 1.5
                final_items.append({
                    'id': f"{base['id']}-{t.upper()}", 'name': base['name'], 'type': 'Screen', 
                    'tier': t, 'price': round(p / 10) * 10 - 1, 'description': f"High-Performance {t} Grade"
                })
    if batteries: final_items.extend(batteries)
    else: final_items.append({'id': f"SRK-{mid[:5]}-BAT".upper(), 'name': f"{mid.replace('-',' ').title()} Battery Kit", 'type': 'Battery', 'tier': 'Pro', 'price': 59.00, 'description': "Long-life battery cell."})
    
    products_data[mid] = final_items

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump({'brands': final_brands, 'products': products_data}, f, indent=2)

print("Master exhaustive sync complete.")
