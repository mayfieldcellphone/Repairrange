import csv
import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

costs_path = 'RR project/leads/RETAIL_PRICE_LIST_READY.csv'
catalog_path = 'selfrepairkit/catalog.json'

brands_data = {
    'Apple': {'id': 'apple', 'name': 'iPhone', 'icon': 'smartphone', 'models': {}},
    'Samsung': {'id': 'samsung', 'name': 'Samsung Galaxy', 'icon': 'tablet', 'models': {}},
    'OPPO': {'id': 'oppo', 'name': 'OPPO', 'icon': 'activity', 'models': {}}
}

products_data = {}

def map_tier(raw_tier):
    raw = raw_tier.lower()
    if "incell" in raw or "lcd" in raw: return "Budget"
    if "original" in raw or "oem" in raw or "service pack" in raw or "pull" in raw: return "Elite"
    return "Pro"

with open(costs_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        brand_name = row['Brand']
        model_string = row['Model']
        part_type = row['Part Type']
        tier_raw = row['Quality Tier']
        retail_price = row['Prospective Retail Price (AUD)'].replace('$', '')
        
        if brand_name not in brands_data:
            continue
            
        # SPLIT MODELS BY SLASH
        individual_models = [m.strip() for m in model_string.split('/')]
        
        for model_raw in individual_models:
            # Skip non-product rows like "Screen Protectors" generic labels if any
            if "Screen Protector" in tier_raw and brand_name == "Apple": continue
            
            model_id = slugify(model_raw)
            
            # Add to brands list
            if model_id not in brands_data[brand_name]['models']:
                brands_data[brand_name]['models'][model_id] = {
                    'id': model_id,
                    'name': model_raw,
                    'image': 'https://sc02.alicdn.com/kf/Ac8c64183dc2a4b9894fa022cce6d4611U.png'
                }
                
            # Add to products data
            if model_id not in products_data:
                products_data[model_id] = []
                
            products_data[model_id].append({
                'id': f"SRK-{model_id[:5]}-{slugify(tier_raw)[:10]}".upper(),
                'name': f"{model_raw} {part_type} Kit - {tier_raw}",
                'type': part_type,
                'tier': map_tier(tier_raw),
                'price': float(retail_price),
                'description': tier_raw
            })

final_brands = []
for b in brands_data.values():
    b_copy = b.copy()
    # Sort models by name
    b_copy['models'] = sorted(list(b['models'].values()), key=lambda x: x['name'])
    final_brands.append(b_copy)

# Preserve accessories
with open(catalog_path, 'r', encoding='utf-8') as f:
    old_cat = json.load(f)
    products_data['accessories'] = old_cat['products'].get('accessories', [])

final_catalog = {
    'brands': final_brands,
    'products': products_data
}

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(final_catalog, f, indent=2)

print("Catalog successfully expanded and populated with all individual models.")
