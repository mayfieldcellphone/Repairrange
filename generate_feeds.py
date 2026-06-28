import json
import csv
import os

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(ROOT_DIR, "selfrepairkit", "catalog.json")
GOOGLE_CSV_PATH = os.path.join(ROOT_DIR, "selfrepairkit", "google_products.csv")
FACEBOOK_CSV_PATH = os.path.join(ROOT_DIR, "selfrepairkit", "facebook_catalog.csv")

BASE_URL = "https://selfrepairkit.com.au/shop.html"
IMAGE_PLACEHOLDER = "https://sc04.alicdn.com/kf/A4698a6c841b14cec8f1ce6fa878c0e0eN.png"

def generate_feeds():
    if not os.path.exists(CATALOG_PATH):
        print("Error: catalog.json not found.")
        return

    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # Prepare Google Feed Header
    google_header = [
        "id", "title", "description", "price", "image_link", 
        "brand", "google_product_category", "link", "condition", "availability"
    ]
    
    # Prepare Facebook Feed Header
    facebook_header = [
        "id", "title", "description", "price", "image_link", 
        "brand", "google_product_category", "link", "condition", "availability"
    ]

    google_rows = []
    
    # Map brand IDs to display names
    brand_display_names = {
        "apple": "Apple",
        "samsung": "Samsung",
        "oppo": "OPPO",
        "google": "Google",
        "accessories": "SelfRepairKit"
    }

    # Process all products
    for model_id, products in catalog['products'].items():
        # Determine Brand from model_id or lookup
        brand_id = "accessories"
        if model_id != "accessories":
            for brand in catalog['brands']:
                for group in brand['groups']:
                    if any(m['id'] == model_id for m in group['models']):
                        brand_id = brand['id']
                        break
                if brand_id != "accessories": break

        brand_name = brand_display_names.get(brand_id, "SelfRepairKit")

        for p in products:
            # Clean up price format
            price_str = f"{float(p['price']):.2f} AUD"
            
            # Construct deep link
            link = f"{BASE_URL}?model={model_id}" if model_id != "accessories" else f"{BASE_URL}?category=accessories"
            
            # Use specific image if available, else fallback
            image = p.get('image', IMAGE_PLACEHOLDER)
            if not image or image == "None":
                image = IMAGE_PLACEHOLDER

            row = {
                "id": p['id'],
                "title": p['name'],
                "description": p.get('description', f"Professional {p.get('type', 'Repair')} Kit for {p['name']}."),
                "price": price_str,
                "image_link": image,
                "brand": brand_name,
                "google_product_category": "Electronics > Communications > Telephony > Mobile Phone Accessories",
                "link": link,
                "condition": "new",
                "availability": "in_stock"
            }
            google_rows.append(row)

    # Write Google CSV
    with open(GOOGLE_CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=google_header)
        writer.writeheader()
        writer.writerows(google_rows)

    # Write Facebook CSV (Same format for now)
    with open(FACEBOOK_CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=facebook_header)
        writer.writeheader()
        writer.writerows(google_rows)

    print(f"Successfully generated feeds with {len(google_rows)} products.")

if __name__ == "__main__":
    generate_feeds()
