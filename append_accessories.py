import openpyxl
import os

file_path = 'SelfRepairKit-Master-Product-Database.xlsx'
sheet_name = 'Master Products'

# Data to append
accessories = [
    {
        "SKU": "ACC-CBL-1M", "Model": "iQuick Braided USB-C (1M)", "Repair Type": "Cable",
        "Quality Tier": "Pro", "Price AUD": 49.00, "Description (Keywords)": "High-speed charging."
    },
    {
        "SKU": "ACC-CBL-6FT", "Model": "Anker 322 Lightning (6ft)", "Repair Type": "Cable",
        "Quality Tier": "Pro", "Price AUD": 35.00, "Description (Keywords)": "Durable braided."
    },
    {
        "SKU": "ACC-CHG-30W", "Model": "iQuick GaN II 30W", "Repair Type": "Charger",
        "Quality Tier": "Pro", "Price AUD": 49.00, "Description (Keywords)": "PD3.0 Adapter."
    },
    {
        "SKU": "ACC-CHG-45W", "Model": "iQuick GaN II 45W", "Repair Type": "Charger",
        "Quality Tier": "Pro", "Price AUD": 69.00, "Description (Keywords)": "Dual USB-C."
    },
    {
        "SKU": "ACC-GLS-S26U", "Model": "Galaxy S26 Ultra Glass", "Repair Type": "Protection",
        "Quality Tier": "Elite", "Price AUD": 29.00, "Description (Keywords)": "Kinglas 3D."
    },
    {
        "SKU": "ACC-TOOL-728B", "Model": "Relife RL-728B Set", "Repair Type": "Tools",
        "Quality Tier": "Elite", "Price AUD": 79.00, "Description (Keywords)": "Pro Screwdrivers."
    },
    {
        "SKU": "ACC-TOOL-METAL", "Model": "Metal Opening Tool", "Repair Type": "Tools",
        "Quality Tier": "Pro", "Price AUD": 9.00, "Description (Keywords)": "Durable steel."
    },
    {
        "SKU": "ACC-CLN-S880", "Model": "PCB Cleaning Liquid", "Repair Type": "Cleaning",
        "Quality Tier": "Pro", "Price AUD": 49.00, "Description (Keywords)": "Technician Grade."
    },
    {
        "SKU": "ACC-CLN-BRUSH", "Model": "Anti-Static Brush", "Repair Type": "Cleaning",
        "Quality Tier": "Pro", "Price AUD": 9.00, "Description (Keywords)": "Protects internals."
    }
]

image_url = "https://sc04.alicdn.com/kf/A4c982a552d694cb6bcf06793a9215eb3u.webp"
brand = "Accessories"
group = "Lab Essentials"

# Load workbook
wb = openpyxl.load_workbook(file_path)
ws = wb[sheet_name]

# Get headers
headers = [cell.value for cell in ws[1]]
header_to_idx = {header: i for i, header in enumerate(headers)}

# Prepare rows
for item in accessories:
    row_data = [None] * len(headers)
    
    # Static values
    if "Brand" in header_to_idx: row_data[header_to_idx["Brand"]] = brand
    if "Group" in header_to_idx: row_data[header_to_idx["Group"]] = group
    if "Image URL" in header_to_idx: row_data[header_to_idx["Image URL"]] = image_url
    
    # Item specific values
    for key, value in item.items():
        if key in header_to_idx:
            row_data[header_to_idx[key]] = value
            
    ws.append(row_data)

# Save
wb.save(file_path)
print(f"Successfully appended {len(accessories)} items to {file_path}")
