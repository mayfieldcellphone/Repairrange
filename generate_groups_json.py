import json
import re

def slugify(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def get_series_group(name, brand_id):
    name = name.lower()
    if brand_id == 'apple':
        match = re.search(r'iphone\s+(\d+)', name)
        if match:
            n = int(match.group(1))
            if n <= 8: return "iPhone 7/8/SE Series"
            return f"iPhone {n} Series"
        if 'se' in name: return "iPhone 7/8/SE Series"
        if 'iphone x' in name: return "iPhone X Series"
    if brand_id == 'samsung':
        match = re.search(r's(\d+)', name)
        if match: return f"Galaxy S{match.group(1)} Series"
        match = re.search(r'a(\d+)', name)
        if match: return "Galaxy A Series"
    if brand_id == 'oppo':
        if 'reno' in name: return "OPPO Reno Series"
        if 'find' in name: return "OPPO Find Series"
        return "OPPO A-Series"
    if brand_id == 'google':
        match = re.search(r'pixel\s+(\d+)', name)
        if match: return f"Pixel {match.group(1)} Series"
        return "Pixel Series"
    return "Other"

catalog_path = 'selfrepairkit/catalog.json'
groups_path = 'selfrepairkit/groups.json'

with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

products = catalog['products']
groups = {}

for brand in catalog['brands']:
    brand_id = brand['id']
    models_to_process = []
    
    if 'models' in brand:
        models_to_process = brand['models']
    elif 'groups' in brand:
        for g in brand['groups']:
            models_to_process.extend(g['models'])

    for model in models_to_process:
        mid = model['id']
        m_name = model['name']
        group_name = get_series_group(m_name, brand_id)
        gid = slugify(group_name)
        
        if gid not in groups:
            groups[gid] = {
                "id": gid,
                "name": group_name,
                "brand": brand_id,
                "models": [],
                "minPrice": 9999,
                "repairs": {}
            }
        
        if m_name not in groups[gid]["models"]:
            groups[gid]["models"].append(m_name)
            
        model_prods = products.get(mid, [])
        for p in model_prods:
            ptype = p['type'].lower().replace(' ', '_')
            tier = p['tier'].lower()
            price = p['price']
            
            if price < groups[gid]["minPrice"]:
                groups[gid]["minPrice"] = price
                
            if ptype not in groups[gid]["repairs"]:
                groups[gid]["repairs"][ptype] = {}
            
            if m_name not in groups[gid]["repairs"][ptype]:
                groups[gid]["repairs"][ptype][m_name] = {}
                
            groups[gid]["repairs"][ptype][m_name][tier] = {
                "price": int(price),
                "sku": p['id']
            }

# Final formatting
output = {
    "batteryUpsellPrice": 49,
    "batteryUpsellNote": "Recommended for devices over 2 years old.",
    "groups": list(groups.values())
}

with open(groups_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f"Generated groups.json with updated repair keys.")
