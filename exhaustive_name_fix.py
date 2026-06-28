import csv
import json
import re

def clean_model_name_v2(text, brand):
    # Common marketing/tech fluff to strip out entirely
    removals = [
        r'(?i)REFURB (Outer|with Frame) (for|for Samsung) ',
        r'(?i)Full Coverage.*for ',
        r'(?i)ASSEMBLED.*for ',
        r'(?i)Screen Replacement.*',
        r'(?i)Replacement Battery.*',
        r'(?i)Battery.*',
        r'(?i)Screen.*',
        r'(?i) with Adhesive.*',
        r'(?i) \d+mAh.*',
        r'(?i) \d+G.*',
        r'(?i) [A-Z]\d+[A-Z].*', # Technical model codes like SM-G998B
        r'(?i) Kit.*',
        r'(?i) -.*',
        r'(?i)Replacement.*',
        r'(?i)Premium.*',
        r'(?i)Genuine.*',
        r'(?i)Aftermarket.*',
        r'(?i)OLED.*',
        r'(?i)LCD.*',
        r'(?i)Incell.*',
        r'(?i)Diagnosable.*',
        r'(?i)Compatible.*',
        r'(?i)Assembly.*',
        r'(?i)Module.*',
        r'(?i)Hard.*',
        r'(?i)Soft.*'
    ]
    
    name = text
    for r in removals:
        name = re.sub(r, '', name)
    
    # Clean technical part codes like GH82-... or internal strings
    name = re.sub(r'(?i)GH\d{2}-\w+', '', name)
    name = re.sub(r'(?i)[XG]\d{3}\w*', '', name)
    
    name = name.strip()

    # Brand specific forced naming
    if brand == "Apple":
        # Ensure it looks like "iPhone 13 Pro Max"
        match = re.search(r'(?i)(iPhone \d+[\s\w]*)', text)
        if match: return match.group(1).strip()
    
    if brand == "Samsung":
        # Strip "Samsung" and "Galaxy" to find the core ID like "S23 Ultra"
        name = re.sub(r'(?i)Samsung ', '', name)
        name = re.sub(r'(?i)Galaxy ', '', name)
        # Match S/A/Note/Z/Fold series
        match = re.search(r'(?i)^([SAZ]|Note|Fold|Flip|Tab|Watch)\d*[\+]?[\s\w]*', name)
        if match:
            core = match.group(0).strip()
            # Special case for Galaxy prefix if it's a mobile
            if re.search(r'^[SAZ]|Note|Fold|Flip', core):
                return "Galaxy " + core
            return core
            
    if brand == "OPPO":
        name = re.sub(r'(?i)OPPO ', '', name)
        return "OPPO " + name.strip()

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
        
        # USE THE NEW CLEANER
        model_name = clean_model_name_v2(full_text, brand)
        if not model_name or len(model_name) < 3: continue
        
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
            
            # Map quality correctly
            raw_t = (tier_raw + " " + full_text).lower()
            tier_cat = "Pro"
            if "incell" in raw_t or "lcd" in raw_t: tier_cat = "Budget"
            elif any(x in raw_t for x in ["original", "oem", "service pack", "pull"]): tier_cat = "Elite"
            
            products_data[mid].append({
                'id': f"SRK-{mid[:5]}-{slugify(tier_raw)[:10]}".upper(),
                'name': f"{m_name} {part_type} Kit",
                'type': part_type,
                'tier': tier_cat,
                'price': calculate_price(cost),
                'description': f"Premium {tier_raw} replacement part."
            })

# Re-group and fill gaps
LABELS = { 'Budget': 'Aftermarket Incell', 'Pro': 'Aftermarket OLED', 'Elite': 'OEM Original' }
final_products = {}
for mid, items in products_data.items():
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
                    'type': 'Screen', 'tier': t, 'price': round(price / 10) * 10 - 1, 'description': f"High-Performance {LABELS[t]}"
                })
    if batteries: final_items.append(batteries[0])
    else: final_items.append({'id': f"SRK-{mid[:5]}-BAT".upper(), 'name': f"{mid.replace('-',' ').title()} Battery Kit", 'type': 'Battery', 'tier': 'Pro', 'price': 59.00, 'description': "Long-life cell."})
    final_products[mid] = final_items

# Final assembly
with open(catalog_path, 'r', encoding='utf-8') as f:
    old = json.load(f)
    final_products['accessories'] = old['products'].get('accessories', [])

final_brands = []
for b_name, b_info in brands_data.items():
    b_info['models'] = sorted(list(b_info['models'].values()), key=lambda x: x['name'])
    final_brands.append(b_info)

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump({'brands': final_brands, 'products': final_products}, f, indent=2)

print("Exhaustive catalog reconstruction with correct names complete.")
