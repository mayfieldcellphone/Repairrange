import json
import re

def clean_final(name):
    # Remove technical codes like GH82-... or X926...
    name = re.sub(r'(?i)GH\d{2}-\w+', '', name)
    name = re.sub(r'(?i)[XG]\d{3}\w*', '', name)
    name = name.replace('Greencell', '').strip()
    # Remove any stray model numbers at the end
    name = re.sub(r'\s+[A-Z]\d+.*', '', name)
    return name.strip()

catalog_path = 'selfrepairkit/catalog.json'

with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for brand in catalog['brands']:
    new_models = []
    seen = set()
    for m in brand['models']:
        clean = clean_final(m['name'])
        # If it's just a code or empty, skip
        if not any(c.isalpha() for c in clean) or len(clean) < 3: continue
        
        if clean not in seen:
            m['name'] = clean
            new_models.append(m)
            seen.add(clean)
    brand['models'] = sorted(new_models, key=lambda x: x['name'])

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2)

print("Final targeted name cleaning complete.")
