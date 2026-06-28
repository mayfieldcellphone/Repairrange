import json
import os
import stripe
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(ROOT_DIR, "selfrepairkit", "catalog.json")
PRICE_MAPPING_PATH = os.path.join(ROOT_DIR, "selfrepairkit", "stripe_prices.json")

def sync_targeted_iphone14():
    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    
    with open(PRICE_MAPPING_PATH, 'r', encoding='utf-8') as f:
        mappings = json.load(f)

    target_models = ["iphone-14", "iphone-14-plus", "iphone-14-pro", "iphone-14-pro-max"]
    
    updated = 0
    for model_id in target_models:
        if model_id not in catalog['products']: continue
        for p in catalog['products'][model_id]:
            # Target OLED (Pro) and Elite tiers
            if p['tier'] not in ['Pro', 'Elite']: continue
            
            sku = p['id']
            new_amount = int(float(p['price']) * 100)
            
            print(f"Checking {sku} ({p['tier']}) -> New target: {new_amount}...")
            
            try:
                # Create new price in Stripe
                new_price = stripe.Price.create(
                    product=sku,
                    unit_amount=new_amount,
                    currency="aud",
                )
                mappings[sku] = new_price.id
                print(f"  + Updated price to {new_price.id} (${p['price']})")
                updated += 1
            except Exception as e:
                print(f"  ! Error: {str(e)}")

    with open(PRICE_MAPPING_PATH, 'w', encoding='utf-8') as f:
        json.dump(mappings, f, indent=2)
    print(f"iPhone 14 sync complete. {updated} prices updated.")

if __name__ == "__main__":
    sync_targeted_iphone14()
