import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def is_requested_model(name, brand_id):
    name = name.lower()
    if brand_id == 'apple':
        # Match iPhone 7 through 18
        match = re.search(r'iphone\s+(\d+|se|x[rs]?)', name)
        if match:
            val = match.group(1)
            if val in ['se', 'x', 'xr', 'xs']: return True
            try:
                num = int(val)
                return 7 <= num <= 18
            except: return False
        return False
    
    if brand_id == 'samsung':
        # Strictly S and A series only (exclude Z, Fold, Flip, Tab, Note)
        # Note: We want to be careful not to match "Tab S" or "Note A"
        if "galaxy s" in name or "galaxy a" in name:
            # Exclude Fold/Flip/Tab/Note if they are also in the name
            if any(x in name for x in ['fold', 'flip', 'tab', 'note', 'watch']): return False
            return True
        # Also match shorthand S22, A54 etc if Galaxy is missing but it's clearly a mobile
        if re.search(r'^[sa]\d+', name): return True
        return False
    
    if brand_id == 'oppo':
        return True # Keeping OPPO as is for now unless specified
        
    return False

catalog_path = 'selfrepairkit/catalog.json'

with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

old_products = catalog['products']
new_brands = []
allowed_model_ids = set()

# 1. Filter Brands & Models
for brand in catalog['brands']:
    clean_models = []
    for m in brand['models']:
        if is_requested_model(m['name'], brand['id']):
            clean_models.append(m)
            allowed_model_ids.add(m['id'])
    
    # Manually ensure S22/S23/S24/S25 series completeness if missing from data
    if brand['id'] == 'samsung':
        series = ['S22', 'S23', 'S24', 'S25', 'S26']
        variants = ['', ' Plus', ' Ultra', ' FE']
        for s in series:
            for v in variants:
                name = f"Galaxy {s}{v}"
                mid = slugify(name)
                if mid not in [x['id'] for x in clean_models]:
                    clean_models.append({
                        'id': mid, 'name': name, 
                        'image': 'https://sc02.alicdn.com/kf/Ac8c64183dc2a4b9894fa022cce6d4611U.png'
                    })
                    allowed_model_ids.add(mid)
                    
    # Manually ensure iPhone 7-18 completeness
    if brand['id'] == 'apple':
        nums = list(range(7, 19))
        variants = ['', ' Plus', ' Pro', ' Pro Max', ' mini']
        for n in nums:
            for v in variants:
                if n < 11 and (v == ' Pro' or v == ' Pro Max'): continue
                if n > 8 and v == ' Plus' and n < 14: continue
                name = f"iPhone {n}{v}"
                mid = slugify(name)
                if mid not in [x['id'] for x in clean_models]:
                    clean_models.append({
                        'id': mid, 'name': name,
                        'image': 'https://sc02.alicdn.com/kf/Ac8c64183dc2a4b9894fa022cce6d4611U.png'
                    })
                    allowed_model_ids.add(mid)

    brand['models'] = sorted(clean_models, key=lambda x: x['name'])
    new_brands.append(brand)

# 2. Filter Products
new_products = {}
LABELS = { 'Budget': 'Aftermarket Incell', 'Pro': 'Aftermarket OLED', 'Elite': 'OEM Original' }

for mid in allowed_model_ids:
    if mid in old_products:
        items = old_products[mid]
    else:
        # Create placeholders for missing models so the UI doesn't crash
        items = []
        
    screens = [p for p in items if p.get('type') == 'Screen']
    batteries = [p for p in items if p.get('type') == 'Battery']
    
    final_items = []
    # Ensure 3 Screen Tiers
    tiers = {p['tier']: p for p in screens}
    base_price = 189.0 if not screens else screens[0]['price']
    
    for t in ['Budget', 'Pro', 'Elite']:
        if t in tiers:
            final_items.append(tiers[t])
        else:
            price = base_price
            if t == 'Budget': price = base_price * 0.6
            if t == 'Elite': price = base_price * 1.4
            # Pricing for future models (iPhone 18, S26) should be high
            if '18' in mid or 's26' in mid: price += 100
            
            final_items.append({
                'id': f"SRK-{mid[:5]}-{t.upper()}".upper(),
                'name': f"{mid.replace('-', ' ').title()} Screen Kit",
                'type': 'Screen', 'tier': t, 'price': round(price / 10) * 10 - 1,
                'description': f"Coming Soon: High-Performance {LABELS[t]} Grade" if ('18' in mid or 's26' in mid) else f"Professional {LABELS[t]} Grade"
            })
            
    # Ensure Battery
    if batteries:
        final_items.append(batteries[0])
    else:
        final_items.append({
            'id': f"SRK-{mid[:5]}-BAT".upper(),
            'name': f"{mid.replace('-',' ').title()} Battery Kit",
            'type': 'Battery', 'tier': 'Pro', 'price': 69.00, 'description': "Long-life high capacity cell."
        })
    new_products[mid] = final_items

new_products['accessories'] = old_products.get('accessories', [])

catalog['brands'] = new_brands
catalog['products'] = new_products

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2)

print("Exhaustive clean of S/A series and iPhone 7-18 complete.")
