import pandas as pd
import os

EXCEL_PATH = "SelfRepairKit-Master-Product-Database.xlsx"

new_accessories = [
    {"SKU": "ACC-CBL-1M", "Brand": "Accessories", "Group": "Lab Essentials", "Model": "iQuick Braided USB-C (1M)", "Repair Type": "Cable", "Quality Tier": "Pro Soft OLED", "Price AUD": 49.00, "Description (Keywords)": "High-speed charging.", "Image URL": "https://sc04.alicdn.com/kf/A4c982a552d694cb6bcf06793a9215eb3u.webp"},
    {"SKU": "ACC-CBL-6FT", "Brand": "Accessories", "Group": "Lab Essentials", "Model": "Anker 322 Lightning (6ft)", "Repair Type": "Cable", "Quality Tier": "Pro Soft OLED", "Price AUD": 35.00, "Description (Keywords)": "Durable braided.", "Image URL": "https://sc04.alicdn.com/kf/A4c982a552d694cb6bcf06793a9215eb3u.webp"},
    {"SKU": "ACC-CHG-30W", "Brand": "Accessories", "Group": "Lab Essentials", "Model": "iQuick GaN II 30W", "Repair Type": "Charger", "Quality Tier": "Pro Soft OLED", "Price AUD": 49.00, "Description (Keywords)": "PD3.0 Adapter.", "Image URL": "https://sc04.alicdn.com/kf/A4c982a552d694cb6bcf06793a9215eb3u.webp"},
    {"SKU": "ACC-CHG-45W", "Brand": "Accessories", "Group": "Lab Essentials", "Model": "iQuick GaN II 45W", "Repair Type": "Charger", "Quality Tier": "Pro Soft OLED", "Price AUD": 69.00, "Description (Keywords)": "Dual USB-C.", "Image URL": "https://sc04.alicdn.com/kf/A4c982a552d694cb6bcf06793a9215eb3u.webp"},
    {"SKU": "ACC-GLS-S26U", "Brand": "Accessories", "Group": "Lab Essentials", "Model": "Galaxy S26 Ultra Glass", "Repair Type": "Protection", "Quality Tier": "Elite OEM Service Pack", "Price AUD": 29.00, "Description (Keywords)": "Kinglas 3D.", "Image URL": "https://sc04.alicdn.com/kf/A4c982a552d694cb6bcf06793a9215eb3u.webp"},
    {"SKU": "ACC-TOOL-728B", "Brand": "Accessories", "Group": "Lab Essentials", "Model": "Relife RL-728B Set", "Repair Type": "Tools", "Quality Tier": "Elite OEM Service Pack", "Price AUD": 79.00, "Description (Keywords)": "Pro Screwdrivers.", "Image URL": "https://sc04.alicdn.com/kf/A4c982a552d694cb6bcf06793a9215eb3u.webp"},
    {"SKU": "ACC-TOOL-METAL", "Brand": "Accessories", "Group": "Lab Essentials", "Model": "Metal Opening Tool", "Repair Type": "Tools", "Quality Tier": "Pro Soft OLED", "Price AUD": 9.00, "Description (Keywords)": "Durable steel.", "Image URL": "https://sc04.alicdn.com/kf/A4c982a552d694cb6bcf06793a9215eb3u.webp"},
    {"SKU": "ACC-CLN-S880", "Brand": "Accessories", "Group": "Lab Essentials", "Model": "PCB Cleaning Liquid", "Repair Type": "Cleaning", "Quality Tier": "Pro Soft OLED", "Price AUD": 49.00, "Description (Keywords)": "Technician Grade.", "Image URL": "https://sc04.alicdn.com/kf/A4c982a552d694cb6bcf06793a9215eb3u.webp"},
    {"SKU": "ACC-CLN-BRUSH", "Brand": "Accessories", "Group": "Lab Essentials", "Model": "Anti-Static Brush", "Repair Type": "Cleaning", "Quality Tier": "Pro Soft OLED", "Price AUD": 9.00, "Description (Keywords)": "Protects internals.", "Image URL": "https://sc04.alicdn.com/kf/A4c982a552d694cb6bcf06793a9215eb3u.webp"}
]

if os.path.exists(EXCEL_PATH):
    try:
        # Load the existing data
        df = pd.read_excel(EXCEL_PATH, sheet_name="Master Products")
        
        # Check for duplicates by SKU
        existing_skus = df['SKU'].tolist()
        to_add = [acc for acc in new_accessories if acc['SKU'] not in existing_skus]
        
        if to_add:
            df_new = pd.concat([df, pd.DataFrame(to_add)], ignore_index=True)
            
            # Save back to Excel
            with pd.ExcelWriter(EXCEL_PATH, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
                df_new.to_excel(writer, sheet_name="Master Products", index=False)
            
            print(f"Successfully added {len(to_add)} accessories to Master Excel.")
        else:
            print("Accessories already exist in Master Excel.")
            
    except Exception as e:
        print(f"Error updating Excel: {str(e)}")
else:
    print(f"Master Excel not found at {EXCEL_PATH}")
