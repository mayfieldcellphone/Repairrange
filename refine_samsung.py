import json
import re

def slugify(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

# Targeted Filter for S and A series only
def is_target_samsung(name):
    name = name.lower()
    # Exclude non-target series
    if any(x in name for x in ['tab', 'note', 'fold', 'flip', 'watch', 'book', 'buds']): return False
    # Match core S and A series
    if re.search(r'galaxy\s+[sa]\d+', name) or re.search(r'^[sa]\d+', name): return True
    return False

def clean_samsung_name(name):
    # Extract just "Galaxy S23 Ultra" etc
    match = re.search(r'(Galaxy\s+[SA]\d+[\+]?\s*\w*)', name, re.IGNORECASE)
    if match: return match.group(1).strip()
    # Fallback for shorthand
    match = re.search(r'([SA]\d+[\+]?\s*\w*)', name, re.IGNORECASE)
    if match: return "Galaxy " + match.group(1).strip()
    return name

catalog_path = 'selfrepairkit/catalog.json'
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# 1. Filter out Samsung non-target models
samsung_brand = next(b for b in catalog['brands'] if b['id'] == 'samsung')
clean_samsung_models = []
seen_ids = set()

for m in samsung_brand['models']:
    if is_target_samsung(m['name']):
        clean_name = clean_samsung_name(m['name'])
        mid = slugify(clean_name)
        if mid not in seen_ids:
            m['id'] = mid
            m['name'] = clean_name
            clean_samsung_models.append(m)
            seen_ids.add(mid)

# Add missing S22 models if not present
s22_series = ["Galaxy S22", "Galaxy S22 Plus", "Galaxy S22 Ultra", "Galaxy S22 FE"]
for name in s22_series:
    mid = slugify(name)
    if mid not in seen_ids:
        clean_samsung_models.append({"id": mid, "name": name, "image": "https://sc02.alicdn.com/kf/Ac8c64183dc2a4b9894fa022cce6d4611U.png"})
        seen_ids.add(mid)

samsung_brand['models'] = sorted(clean_models, key=lambda x: x['name']) # wait, logic error in var name
# Correcting logic below
