import pandas as pd
import json
import os
import re

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(ROOT_DIR, "SelfRepairKit-Master-Product-Database.xlsx")
CATALOG_PATH = os.path.join(ROOT_DIR, "selfrepairkit", "catalog.json")
GROUPS_PATH = os.path.join(ROOT_DIR, "selfrepairkit", "groups.json")

def slugify(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def sync_excel_to_web():
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: Master Excel not found at {EXCEL_PATH}")
        return False

    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name="Master Products")
        
        # --- 1. Prepare Data for catalog.json (Old SEO pages/Rotation) ---
        brands_map = {
            'Apple': {'id': 'apple', 'name': 'iPhone Kit', 'icon': 'smartphone', 'groups': {}},
            'Samsung': {'id': 'samsung', 'name': 'Samsung Kit', 'icon': 'tablet', 'groups': {}},
            'OPPO': {'id': 'oppo', 'name': 'OPPO Kit', 'icon': 'monitor-smartphone', 'groups': {}},
            'Google': {'id': 'google', 'name': 'Pixel Kit', 'icon': 'chrome', 'groups': {}},
            'Accessories': {'id': 'accessories', 'name': 'Accessories', 'icon': 'package', 'groups': {}}
        }
        products_data = {'accessories': []} 
        
        # --- 2. Prepare Data for groups.json (Shop Wizard) ---
        groups_data = {
            "batteryUpsellPrice": 49,
            "batteryUpsellNote": "Recommended for devices over 2 years old.",
            "groups": []
        }
        wizard_groups = {} # id -> group object

        TIER_MAP = {
            'Budget INCELL LCD': 'budget',
            'Pro Soft OLED': 'pro',
            'Elite OEM Service Pack': 'elite',
            'Standard Battery': 'standard',
            'Diagnosable Battery': 'diagnosable'
        }

        for _, row in df.iterrows():
            brand_name = str(row['Brand']).strip()
            model_name = str(row['Model']).strip()
            group_name = str(row['Group']).strip()
            repair_type_raw = str(row['Repair Type']).strip()
            quality_tier_raw = str(row['Quality Tier']).strip()
            price = float(row['Price AUD'])
            sku = str(row['SKU']).strip()
            image_url = str(row['Image URL']).strip()
            description = str(row['Description (Keywords)']).strip()

            if brand_name not in brands_map: continue

            # --- Catalog Logic ---
            model_id = slugify(model_name)
            group_id = slugify(group_name)
            
            # --- Wizard Logic (groups.json) ---
            if brand_name != 'Accessories':
                if group_id not in wizard_groups:
                    wizard_groups[group_id] = {
                        "id": group_id,
                        "name": group_name,
                        "brand": brand_name.lower(),
                        "models": [],
                        "minPrice": 999,
                        "repairs": {"screen": {}, "battery": {}, "charging_port": {}}
                    }
                
                g = wizard_groups[group_id]
                if model_name not in g["models"]:
                    g["models"].append(model_name)
                
                if price < g["minPrice"]:
                    g["minPrice"] = int(price)
                
                repair_key = slugify(repair_type_raw)
                if repair_key == 'charging-port': repair_key = 'charging_port'
                
                if model_name not in g["repairs"][repair_key]:
                    g["repairs"][repair_key][model_name] = {}
                
                tier_key = 'pro'
                for k, v in TIER_MAP.items():
                    if k.lower() in quality_tier_raw.lower():
                        tier_key = v
                        break
                
                g["repairs"][repair_key][model_name][tier_key] = {
                    "price": int(price),
                    "sku": sku
                }

            # --- Backwards compatibility for catalog.json ---
            if model_id not in products_data: products_data[model_id] = []
            products_data[model_id].append({
                "id": sku, "name": f"{model_name} {repair_type_raw} Kit", 
                "type": repair_type_raw, "tier": tier_key.capitalize(), 
                "price": price, "description": description, "image": image_url
            })

        # Save groups.json
        groups_data["groups"] = list(wizard_groups.values())
        with open(GROUPS_PATH, 'w', encoding='utf-8') as f:
            json.dump(groups_data, f, indent=2)
        print(f"Success: Updated {GROUPS_PATH}")

        # Save catalog.json (minimal version for now)
        with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
            json.dump({"products": products_data}, f, indent=2)
        print(f"Success: Updated {CATALOG_PATH}")

        return True
    except Exception as e:
        print(f"Sync failed: {str(e)}")
        return False

if __name__ == "__main__":
    sync_excel_to_web()
