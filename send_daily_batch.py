import csv
import os
import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime

# Define paths - Workspace root contains "RR project"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(ROOT_DIR, "RR project")
CSV_PATH = os.path.join(WORKSPACE_DIR, "leads", "outreach_schedule_june_2026.csv")
LOG_PATH = os.path.join(WORKSPACE_DIR, "strategy", "outreach_log.txt")

# Load local .env if exists
env_path = os.path.join(ROOT_DIR, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key] = val

# Configuration for Hostinger SMTP (No API Keys needed! Bypasses Resend domain block)
SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465 # SSL
SENDER_EMAIL = "info@repairrange.io"
SENDER_NAME = "Khalil"
# Hostinger Professional Mailbox Password
SMTP_PASSWORD = os.environ.get("REPAIRRANGE_SMTP_PASSWORD", "YOUR_MAILBOX_PASSWORD") 

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
        f"P.S. If you're looking to streamline your invoicing and ticketing, check out RepairBill — "
        f"the AI-powered shop management software I also built for the industry: https://repairbill.shop\n\n"
        f"Best regards,\n\n"
        f"Khalil\n"
        f"RepairRange / Mayfield Phone Repair, Newcastle"
    )

def send_email_smtp(to_email, subject, body):
    if SMTP_PASSWORD == "YOUR_MAILBOX_PASSWORD":
        log_message("ERROR: SMTP Password is not configured. Please set the REPAIRRANGE_SMTP_PASSWORD environment variable.")
        return False
        
    try:
        # Construct MIME Message
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = f'"{SENDER_NAME}" <{SENDER_EMAIL}>'
        msg["To"] = to_email

        # Connect to Hostinger SMTP via secure SSL
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.login(SENDER_EMAIL, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, [to_email], msg.as_string())
            
        log_message(f"Successfully sent email to {to_email} via Hostinger SMTP.")
        return True
            
    except smtplib.SMTPAuthenticationError:
        log_message(f"FAILED to authenticate with Hostinger SMTP server for {SENDER_EMAIL}. Check mailbox password.")
        return False
    except Exception as e:
        log_message(f"Unexpected SMTP error sending email to {to_email}: {str(e)}")
        return False

def main():
    log_message("Starting daily outreach email batch processing via Hostinger SMTP.")
    
    # Use a target date (CLI arg or today)
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
        # Check both "Pending" and "Failed" from previous runs on this date to support manual retries
        if row["Scheduled Date"] == target_date_str and (row["Status"] == "Pending" or row["Status"] == "Failed"):
            shop_name = row["Shop Name"]
            city = row["City"]
            email = row["Email"]
            subject = f"Free listing on RepairRange.io — {city} repair pricing guide"
            body = get_email_body(shop_name, city)
            
            log_message(f"Attempting to send email to {shop_name} ({email}) in {city}...")
            
            success = send_email_smtp(email, subject, body)
            if success:
                row["Status"] = "Sent"
                row["Date Sent"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                emails_sent_count += 1
            else:
                row["Status"] = "Failed"
                emails_failed_count += 1
                
        updated_rows.append(row)
        
    with open(CSV_PATH, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated_rows)
        
    log_message(f"Batch completed: {emails_sent_count} successfully sent, {emails_failed_count} failed via Hostinger SMTP.")

if __name__ == "__main__":
    main()
