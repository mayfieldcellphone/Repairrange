import csv
import re

def calculate_retail_price(cost):
    try:
        # UPDATED Strategy: (Diamond Cost + $39 Toolset Value) * 1.4 margin
        price = (float(cost) + 39) * 1.4
        # Round to nearest $9 for premium e-commerce feel (e.g., .00, .49, or .99)
        # We will round to nearest 10 and subtract 1
        rounded = round(price / 10) * 10 - 1
        return f"{rounded:.2f}"
    except:
        return "0.00"

input_path = 'RR project/leads/crazyparts_costs_master.csv'
output_path = 'RR project/leads/RETAIL_PRICE_LIST_READY.csv'

with open(input_path, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    
    # Define Google Sheet friendly headers
    fieldnames = ['Brand', 'Model', 'Part Type', 'Quality Tier', 'Diamond Cost (ex GST)', 'Prospective Retail Price (AUD)']
    
    with open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            cost = row['Your Cost (Diamond Price)']
            retail = calculate_retail_price(cost)
            
            writer.writerow({
                'Brand': row['Brand'],
                'Model': row['Model Name'],
                'Part Type': row['Part Type'],
                'Quality Tier': row['Quality/Tier'],
                'Diamond Cost (ex GST)': f"${cost}",
                'Prospective Retail Price (AUD)': f"${retail}"
            })

print(f"Retail Price List (with $39 toolset) generated successfully at: {output_path}")
