import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def get_series_group(model_name, brand_id):
    name = model_name.lower()
    if brand_id == 'apple':
        match = re.search(r'iphone\s+(\d+|se|x[rs]?)', name)
        if match:
            val = match.group(1)
            if val in ['se', 'x', 'xr', 'xs']: return "iPhone X/SE Series"
            try:
                num = int(val)
                if num <= 8: return "iPhone 7/8/SE Series"
                if 11 <= num <= 11: return "iPhone 11 Series"
                if 12 <= num <= 12: return "iPhone 12 Series"
                if 13 <= num <= 13: return "iPhone 13 Series"
                if 14 <= num <= 14: return "iPhone 14 Series"
                if 15 <= num <= 17: return f"iPhone {num} Series"
                if num == 18: return "iPhone 18 (Coming Soon)"
            except: pass
        return "iPhone Legacy"
    
    if brand_id == 'samsung':
        if "galaxy s" in name:
            match = re.search(r's(\d+)', name)
            if match:
                num = int(match.group(1))
                if 21 <= num <= 24: return "Galaxy S21-S24 Series"
                if 25 <= num <= 26: return f"Galaxy S{num} Series"
            return "Galaxy S Series"
        if "galaxy a" in name: return "Galaxy A Series"
        return "Samsung Other"
        
    if brand_id == 'oppo':
        if "find" in name: return "OPPO Find Series"
        if "reno" in name: return "OPPO Reno Series"
        if "a" in name: return "OPPO A-Series"
        return "OPPO Other"
        
    return "Other"

catalog_path = 'selfrepairkit/catalog.json'

with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

new_brands = []
for brand in catalog['brands']:
    groups = {}
    for m in brand['models']:
        group_name = get_series_group(m['name'], brand['id'])
        if group_name not in groups:
            groups[group_name] = {'id': slugify(group_name), 'name': group_name, 'models': []}
        groups[group_name]['models'].append(m)
    
    brand['groups'] = list(groups.values())
    new_brands.append(brand)

catalog['brands'] = new_brands

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2)

print("Catalog grouped by series successfully.")
