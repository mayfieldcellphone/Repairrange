import csv
import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def calculate_price(cost):
    try:
        c = float(cost)
        # Retail Price = (Cost + $25 Toolset) * 1.4, rounded to nearest $9
        price = (c + 25) * 1.4
        rounded = round(price / 10) * 10 - 1
        return float(rounded)
    except:
        return 0.0

costs_path = 'RR project/leads/crazyparts_costs_master.csv'
catalog_path = 'selfrepairkit/catalog.json'

brands_data = {
    'Apple': {'id': 'apple', 'name': 'iPhone', 'icon': 'smartphone', 'models': {}},
    'Samsung': {'id': 'samsung', 'name': 'Samsung Galaxy', 'icon': 'tablet', 'models': {}},
    'OPPO': {'id': 'oppo', 'name': 'OPPO', 'icon': 'activity', 'models': {}}
}

products_data = {}

with open(costs_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        brand_name = row['Brand']
        model_raw = row['Model Name']
        part_type = row['Part Type']
        tier_raw = row['Quality/Tier']
        cost = row['Your Cost (Diamond Price)']
        
        if brand_name not in brands_data:
            continue
            
        # Basic cleaning for model names
        # Handle cases like "iPhone 12 / 12 mini..." - usually it's better to pick the first or keep as is.
        # Let's keep it as is but slugify for ID
        model_id = slugify(model_raw)
        
        # Add to brands list
        if model_id not in brands_data[brand_name]['models']:
            brands_data[brand_name]['models'][model_id] = {
                'id': model_id,
                'name': model_raw,
                'image': 'https://sc02.alicdn.com/kf/Ac8c64183dc2a4b9894fa022cce6d4611U.png' # Default placeholder
            }
            
        # Add to products data
        if model_id not in products_data:
            products_data[model_id] = []
            
        retail_price = calculate_price(cost)
        
        # Map quality tiers to your categories
        tier = "Pro"
        if "OEM" in tier_raw or "Service Pack" in tier_raw:
            tier = "Elite"
        elif "Incell" in tier_raw:
            tier = "Budget"
            
        products_data[model_id].append({
            'id': f"SRK-{model_id[:5]}-{slugify(tier_raw)[:10]}".upper(),
            'name': f"{model_raw} {part_type} Kit - {tier_raw}",
            'type': part_type,
            'tier': tier,
            'price': retail_price,
            'description': tier_raw
        })

# Final structure
final_brands = []
for b in brands_data.values():
    b_copy = b.copy()
    b_copy['models'] = list(b['models'].values())
    final_brands.append(b_copy)

# Add existing accessories and custom from previous catalog
# (Manual merge to ensure consistency)
with open(catalog_path, 'r', encoding='utf-8') as f:
    old_cat = json.load(f)
    products_data['accessories'] = old_cat['products'].get('accessories', [])
    products_data['custom'] = old_cat['products'].get('custom', [])

final_catalog = {
    'brands': final_brands,
    'products': products_data
}

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(final_catalog, f, indent=2)

print("Catalog successfully updated with all models and calculated prices.")
