import json
import os
import stripe
from dotenv import load_dotenv

# Load keys
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(ROOT_DIR, "selfrepairkit", "catalog.json")
PRICE_MAPPING_PATH = os.path.join(ROOT_DIR, "selfrepairkit", "stripe_prices.json")

def sync_products():
    if not os.path.exists(CATALOG_PATH):
        print("Error: catalog.json not found.")
        return

    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # Load existing mappings if any
    mappings = {}
    if os.path.exists(PRICE_MAPPING_PATH):
        with open(PRICE_MAPPING_PATH, 'r', encoding='utf-8') as f:
            mappings = json.load(f)

    print(f"Starting Stripe Sync for {len(catalog['products'])} model categories...")
    
    count = 0
    errors = 0

    for model_id, products in catalog['products'].items():
        for p in products:
            sku = p['id']

            try:
                # 1. Create or Get Product
                # We use the SKU as the product ID in Stripe for 1:1 mapping
                stripe_product = None
                try:
                    stripe_product = stripe.Product.retrieve(sku)
                    print(f"  - Found existing product: {sku}")
                except stripe.error.InvalidRequestError:
                    # Create if not found
                    stripe_product = stripe.Product.create(
                        id=sku,
                        name=p['name'],
                        description=p.get('description', '')[:500],
                        images=[p.get('image')] if p.get('image') else []
                    )
                    print(f"  + Created product: {sku}")

                # 2. Create Price
                # Prices are immutable in Stripe, so we create a new one if needed
                # For simplicity, we create one and map it. 
                # If price changes in Excel, we'd need to create a new price ID.
                
                # Check if current mapped price ID is still valid for the current price
                existing_price_id = mappings.get(sku)
                if existing_price_id:
                    try:
                        price_obj = stripe.Price.retrieve(existing_price_id)
                        if price_obj.unit_amount == int(float(p['price']) * 100):
                            continue # Price matches, skip
                    except:
                        pass

                new_price = stripe.Price.create(
                    product=sku,
                    unit_amount=int(float(p['price']) * 100),
                    currency="aud",
                )
                
                mappings[sku] = new_price.id
                count += 1
                if count % 10 == 0:
                    print(f"--- Processed {count} items ---")
                    # Save progress
                    with open(PRICE_MAPPING_PATH, 'w', encoding='utf-8') as f:
                        json.dump(mappings, f, indent=2)

            except Exception as e:
                print(f"  ! Error syncing {sku}: {str(e)}")
                errors += 1

    # Final Save
    with open(PRICE_MAPPING_PATH, 'w', encoding='utf-8') as f:
        json.dump(mappings, f, indent=2)

    print(f"\nSync Complete. {count} new prices created. {errors} errors.")

if __name__ == "__main__":
    sync_products()
