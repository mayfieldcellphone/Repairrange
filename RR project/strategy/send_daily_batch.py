import csv
import os
import sys
import json
import subprocess
from datetime import datetime

# Define base paths
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(WORKSPACE_DIR, "leads", "outreach_schedule_june_2026.csv")
LOG_PATH = os.path.join(WORKSPACE_DIR, "strategy", "outreach_log.txt")

SENDER_EMAIL = "support@selfrepairkit.com.au"

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(formatted)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def get_email_body(shop_name, city):
    return (
        f"Hi {shop_name} Team,\n\n"
        f"I run RepairRange.io — an independent phone repair pricing guide covering {city}. "
        f"We're currently adding verified local shop listings, and I'd love to include {shop_name}.\n\n"
        f"Your first month is completely free — you can view our plans and apply directly here:\n"
        f"👉 https://www.repairrange.io/list-your-shop.html\n\n"
        f"What you get: Your shop featured prominently on our {city} pricing page, putting you "
        f"directly in front of local customers actively searching for repair costs. There are no "
        f"commissions and no per-click charges — just a simple, flat listing fee starting at $29/quarter.\n\n"
        f"Best regards,\n\n"
        f"Khalil\n"
        f"RepairRange / Mayfield Phone Repair, Newcastle"
    )

def send_email(to_email, subject, body):
    # Construct the JSON payload for send_gmail_message tool
    payload = {
        "user_google_email": SENDER_EMAIL,
        "to": to_email,
        "subject": subject,
        "body": body,
        "body_format": "text"
    }
    
    # We serialize payload into json string
    payload_str = json.dumps(payload, ensure_ascii=False)
    
    # Construct the command to run accio-mcp-cli call send_gmail_message
    command = ["accio-mcp-cli", "call", "send_gmail_message", "--json", payload_str]
    
    try:
        # Run command with subprocess
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, encoding="utf-8")
        log_message(f"Successfully sent email to {to_email}. Stdout: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"FAILED to send email to {to_email}. Error: {e.stderr.strip()}")
        return False
    except Exception as e:
        log_message(f"Unexpected error sending email to {to_email}: {str(e)}")
        return False

def main():
    log_message("Starting daily outreach email batch processing.")
    
    # Parse date argument if provided, otherwise default to today
    if len(sys.argv) > 1:
        target_date_str = sys.argv[1]
    else:
        target_date_str = datetime.now().strftime("%Y-%m-%d")
        
    log_message(f"Target schedule date: {target_date_str}")
    
    if not os.path.exists(CSV_PATH):
        log_message(f"Error: Lead schedule CSV file not found at {CSV_PATH}")
        sys.exit(1)
        
    rows = []
    headers = []
    emails_sent_count = 0
    emails_failed_count = 0
    
    with open(CSV_PATH, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        for row in reader:
            rows.append(row)
            
    updated_rows = []
    for row in rows:
        # Check if the lead matches the target date and is still pending
        if row["Scheduled Date"] == target_date_str and row["Status"] == "Pending":
            shop_name = row["Shop Name"]
            city = row["City"]
            email = row["Email"]
            subject = f"Free listing on RepairRange.io — {city} repair pricing guide"
            body = get_email_body(shop_name, city)
            
            log_message(f"Attempting to send email to {shop_name} ({email}) in {city}...")
            
            success = send_email(email, subject, body)
            if success:
                row["Status"] = "Sent"
                row["Date Sent"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                emails_sent_count += 1
            else:
                row["Status"] = "Failed"
                emails_failed_count += 1
                
        updated_rows.append(row)
        
    # Write back the updated rows to CSV
    with open(CSV_PATH, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated_rows)
        
    log_message(f"Batch completed: {emails_sent_count} successfully sent, {emails_failed_count} failed.")

if __name__ == "__main__":
    main()
