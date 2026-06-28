import pandas as pd
import requests
import os
from io import StringIO
from datetime import datetime

# CONFIG
SHEET_ID = "1TZ4wELPwdl__5Rmftuavzi-gNE904YAkbTJCZO1p-tg" # The ID you provided earlier
TAB_NAME = "Leads"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(ROOT_DIR, "RR project", "leads", "outreach_schedule_june_2026.csv")

def sync_leads():
    print("🔄 Connecting to Google Sheet...")
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={TAB_NAME}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Failed to reach Google Sheet. Status: {response.status_code}")
            return

        # Read remote leads
        new_leads_df = pd.read_csv(StringIO(response.text))
        if new_leads_df.empty:
            print("📭 No leads found in the cloud sheet.")
            return

        # Load local CRM leads
        if os.path.exists(CSV_PATH):
            local_df = pd.read_csv(CSV_PATH)
        else:
            local_df = pd.DataFrame(columns=["Shop Name", "City", "Email", "Scheduled Day", "Scheduled Date", "Status", "Date Sent"])

        added_count = 0
        
        # Mapping: Web Leads -> local CRM Format
        # Web columns: Timestamp, Shop Name, Suburb, Contact, Phone, Email, Website, Tier, Services, Source City, Page, Status
        for _, row in new_leads_df.iterrows():
            email = str(row.get('Email', '')).strip()
            
            # Check if lead already exists in local CRM (avoid duplicates)
            if email and not local_df[local_df['Email'] == email].empty:
                continue

            # Create new row for local CRM
            new_row = {
                "Shop Name": row.get('Shop Name', 'Unknown Shop'),
                "City": row.get('Suburb', 'Unknown'),
                "Email": email,
                "Scheduled Day": "Web Lead",
                "Scheduled Date": datetime.now().strftime("%Y-%m-%d"),
                "Status": "Incoming",
                "Date Sent": ""
            }
            
            local_df = pd.concat([local_df, pd.DataFrame([new_row])], ignore_index=True)
            added_count += 1

        if added_count > 0:
            local_df.to_csv(CSV_PATH, index=False)
            print(f"✅ Successfully synced {added_count} new leads to RepairRange Hub CRM!")
        else:
            print("✨ Everything is up to date. No new leads found.")

    except Exception as e:
        print(f"❌ Error during sync: {str(e)}")

if __name__ == "__main__":
    sync_leads()
