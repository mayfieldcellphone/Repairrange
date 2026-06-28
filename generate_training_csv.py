import pandas as pd
import os

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(ROOT_DIR, "SelfRepairKit-Master-Product-Database.xlsx")
CSV_OUTPUT = os.path.join(ROOT_DIR, "MASTER_TRAINING_DATA.csv")

def create_training_csv():
    if not os.path.exists(EXCEL_PATH):
        print("Error: Master Excel file not found.")
        return

    print("Reading Master Data Sheet...")
    df = pd.read_excel(EXCEL_PATH)

    # Mapping and Cleaning
    # Brand, Model, Repair_Type, Quality_Tier, Price_AUD, Warranty, Stock_Status, Description
    training_df = pd.DataFrame()
    training_df['Brand'] = df['Brand']
    training_df['Model'] = df['Model']
    training_df['Repair_Type'] = df['Repair Type']
    training_df['Quality_Tier'] = df['Quality Tier']
    training_df['Price_AUD'] = df['Price AUD']
    training_df['Warranty'] = "90 Days" # Default rule
    training_df['Stock_Status'] = df['Stock Status']
    training_df['Description'] = df['Description (Keywords)']

    # Save to CSV
    training_df.to_csv(CSV_OUTPUT, index=False)
    print(f"Created training CSV with {len(training_df)} items.")

if __name__ == "__main__":
    create_training_csv()
