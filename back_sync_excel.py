import pandas as pd
import json
import os

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(ROOT_DIR, "SelfRepairKit-Master-Product-Database.xlsx")
CATALOG_PATH = os.path.join(ROOT_DIR, "selfrepairkit", "catalog.json")

def back_sync_catalog_to_excel():
    if not os.path.exists(CATALOG_PATH):
        print(f"Error: Catalog not found at {CATALOG_PATH}")
        return False
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: Master Excel not found at {EXCEL_PATH}")
        return False

    try:
        # 1. Load the website's live prices
        with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        
        # Flatten all products into a SKU -> Price mapping
        live_prices = {}
        for mid, prods in catalog['products'].items():
            for p in prods:
                if 'id' in p and 'price' in p:
                    live_prices[str(p['id']).strip()] = float(p['price'])

        # 2. Load the Master Excel
        df = pd.read_excel(EXCEL_PATH, sheet_name="Master Products")
        
        # 3. Update Excel prices from live catalog
        updated_count = 0
        for idx, row in df.iterrows():
            sku = str(row['SKU']).strip()
            if sku in live_prices:
                new_price = live_prices[sku]
                if float(row['Price AUD']) != new_price:
                    df.at[idx, 'Price AUD'] = new_price
                    updated_count += 1

        # 4. Save the updated Excel
        if updated_count > 0:
            with pd.ExcelWriter(EXCEL_PATH, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name="Master Products", index=False)
            print(f"SUCCESS: Back-synced {updated_count} selling prices from Website to Master Excel.")
        else:
            print("INFO: Excel already matches live Website prices. No changes needed.")
        
        return True

    except Exception as e:
        print(f"ERROR: Back-sync failed: {str(e)}")
        return False

if __name__ == "__main__":
    back_sync_catalog_to_excel()
