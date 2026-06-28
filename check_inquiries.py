import os
import csv
import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime

# Path definitions
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(ROOT_DIR, "RR project")
CSV_PATH = os.path.join(WORKSPACE_DIR, "leads", "outreach_schedule_june_2026.csv")
CRM_DASHBOARD_PATH = os.path.join(WORKSPACE_DIR, "leads", "crm_dashboard.md")

# Load local .env if exists
env_path = os.path.join(ROOT_DIR, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key] = val

# Credentials
IMAP_SERVER = "imap.hostinger.com"
IMAP_PORT = 993

MAILBOXES = [
    {
        "email": "info@repairrange.io",
        "password": os.environ.get("REPAIRRANGE_SMTP_PASSWORD"),
        "source": "RepairRange Directory"
    },
    {
        "email": "info@repairbill.shop",
        "password": "RepairBill@2026!",
        "source": "RepairBill Platform"
    }
]

def log_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def clean_header(header_val):
    if not header_val:
        return ""
    try:
        decoded = decode_header(header_val)
        parts = []
        for text, codec in decoded:
            if isinstance(text, bytes):
                parts.append(text.decode(codec or "utf-8", errors="ignore"))
            else:
                parts.append(str(text))
        return "".join(parts)
    except Exception as e:
        return str(header_val)

def parse_body_fields(body_text):
    """Extracts key-value pairs from Web3Forms registration emails."""
    fields = {}
    lines = body_text.split("\n")
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip().replace("**", "").replace("_", " ").lower()
            val = parts[1].strip()
            if key and val:
                fields[key] = val
    return fields

def update_lead_status(email_addr, new_status, extra_data=None):
    """Updates lead status in the CSV lead schedule database."""
    if not os.path.exists(CSV_PATH):
        return False
    
    updated = False
    rows = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row.get("Email", "").strip().lower() == email_addr.strip().lower():
                row["Status"] = new_status
                row["Date Sent"] = datetime.now().strftime("%Y-%m-%d")
                updated = True
            rows.append(row)
            
    if updated:
        with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            
    return updated

def add_new_lead_to_csv(lead_data, source="Direct Signup"):
    """Appends a new direct signup lead to our outreach schedule."""
    if not os.path.exists(CSV_PATH):
        return
    
    # Read headers to maintain exact CSV structure
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        
    # Construct row matching: Shop Name,City,Email,Scheduled Day,Scheduled Date,Status,Date Sent
    row_dict = {h: "" for h in headers}
    row_dict["Shop Name"] = lead_data.get("shop name") or lead_data.get("shop_name") or "Unknown Shop"
    row_dict["City"] = (lead_data.get("city page") or lead_data.get("city") or "Sydney").capitalize()
    row_dict["Email"] = lead_data.get("email") or lead_data.get("email address") or ""
    row_dict["Scheduled Day"] = "Direct"
    row_dict["Scheduled Date"] = datetime.now().strftime("%Y-%m-%d")
    row_dict["Status"] = "Trial"
    row_dict["Date Sent"] = datetime.now().strftime("%Y-%m-%d")
    
    if not row_dict["Email"]:
        return # Skip if email is empty
        
    # Check if duplicate email already exists in CSV
    already_exists = False
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Email", "").strip().lower() == row_dict["Email"].strip().lower():
                already_exists = True
                break
                
    if not already_exists:
        with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writerow(row_dict)
        log_message(f"Appended new direct signup to CSV: {row_dict['Shop Name']} ({row_dict['Email']})")

def rebuild_crm_dashboard():
    """Regenerates crm_dashboard.md statistics based on the latest CSV data."""
    if not os.path.exists(CSV_PATH) or not os.path.exists(CRM_DASHBOARD_PATH):
        return
    
    # Count totals
    total_sourced = 0
    pending_count = 0
    failed_count = 0
    trial_count = 0
    replied_count = 0
    sent_count = 0
    
    # Store categorised leads to display
    pending_leads = []
    sent_leads = []
    trial_leads = []
    replied_leads = []
    failed_leads = []
    
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_sourced += 1
            status = row.get("Status", "Pending").strip()
            shop = row.get("Shop Name", "Unknown Shop")
            email_addr = row.get("Email", "")
            city = row.get("City", "Sydney")
            date_info = row.get("Scheduled Date", "") or row.get("Date Sent", "")
            
            lead_line = f"* **{shop}** | `{email_addr}` | City: {city}"
            
            if status == "Pending":
                pending_count += 1
                pending_leads.append(lead_line)
            elif status == "Sent":
                sent_count += 1
                sent_leads.append(lead_line)
            elif status == "Trial" or status == "Signed Up" or status == "Active Trial":
                trial_count += 1
                trial_leads.append(lead_line)
            elif status == "Replied":
                replied_count += 1
                replied_leads.append(lead_line)
            else:  # "Failed" or "Bounced"
                failed_count += 1
                failed_leads.append(lead_line)
                
    # Read the template/dashboard content
    with open(CRM_DASHBOARD_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Rebuild Pipeline Funnel Overview Block
    funnel_text = f"""## 📊 Pipeline Funnel Overview

```text
[Pending]      {"█" * int(round(pending_count * 25 / max(total_sourced, 1)))}{"-" * (25 - int(round(pending_count * 25 / max(total_sourced, 1))))} {pending_count} Leads
[Sent]         {"█" * int(round(sent_count * 25 / max(total_sourced, 1)))}{"-" * (25 - int(round(sent_count * 25 / max(total_sourced, 1))))} {sent_count} Leads
[Active Trial] {"█" * int(round(trial_count * 25 / max(total_sourced, 1)))}{"-" * (25 - int(round(trial_count * 25 / max(total_sourced, 1))))} {trial_count} Leads
[Replied]      {"█" * int(round(replied_count * 25 / max(total_sourced, 1)))}{"-" * (25 - int(round(replied_count * 25 / max(total_sourced, 1))))} {replied_count} Leads
[Failed/Bounce] {"█" * int(round(failed_count * 25 / max(total_sourced, 1)))}{"-" * (25 - int(round(failed_count * 25 / max(total_sourced, 1))))} {failed_count} Leads
```

### Conversion Pipeline Summary
* **Sourced Leads:** {total_sourced}
* **Outreach Attempted:** {sent_count + trial_count + replied_count + failed_count} / {total_sourced} ({int(round((sent_count + trial_count + replied_count + failed_count) * 100 / max(total_sourced, 1)))}%)
* **Bounced / Invalid:** {failed_count} / {total_sourced} ({int(round(failed_count * 100 / max(total_sourced, 1)))}%)
* **Active Free Trials (Month 1):** {trial_count}
* **Paid Active Directory listings:** 0
* **Monthly Recurring Revenue (MRR Equivalent):** ${trial_count * 9.66:.2f} / Month (Estimated conversion target)"""

    # Replace everything between ## 📊 Pipeline Funnel Overview and --- using regex
    content = re.sub(r"## 📊 Pipeline Funnel Overview.*?(?=\n\n---)", funnel_text, content, flags=re.DOTALL)

    # Rebuild Stage-by-Stage Lead Pipeline Lists
    def format_stage_leads(leads, empty_msg):
        return "\n".join(leads) if leads else empty_msg

    pending_section = f"### Stage 1: Pending Outreach ({pending_count} Leads)\n" + format_stage_leads(pending_leads, "* *No leads currently in this stage.*")
    sent_section = f"### Stage 2: Outreach Sent ({sent_count} Leads)\n" + format_stage_leads(sent_leads, "* *No leads currently in this stage.*")
    trial_section = f"### Stage 3: Active Free Trial ({trial_count} Leads)\n" + format_stage_leads(trial_leads, "* *No leads currently in this stage.*")
    replied_section = f"### Stage 4: Paid Active Directory Subscriber ({replied_count} Leads)\n" + format_stage_leads(replied_leads, "* *No leads currently in this stage.*")
    failed_section = f"### Stage 5: Bounced / Failed / Closed Lost ({failed_count} Leads)\n" + format_stage_leads(failed_leads, "* *No leads currently in this stage.*")

    # Replace the Stage sections
    content = re.sub(r"### Stage 1: Pending Outreach.*?(?=\n\n###|\n\n---)", pending_section, content, flags=re.DOTALL)
    content = re.sub(r"### Stage 2: Outreach Sent.*?(?=\n\n###|\n\n---)", sent_section, content, flags=re.DOTALL)
    content = re.sub(r"### Stage 3: Active Free Trial.*?(?=\n\n###|\n\n---)", trial_section, content, flags=re.DOTALL)
    content = re.sub(r"### Stage 4: Paid Active Directory Subscriber.*?(?=\n\n###|\n\n---)", replied_section, content, flags=re.DOTALL)
    content = re.sub(r"### Stage 5: Bounced / Failed / Closed Lost.*?(?=\n\n###|\n\n---)", failed_section, content, flags=re.DOTALL)

    with open(CRM_DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    log_message("Successfully rebuilt crm_dashboard.md with latest conversion stats.")

def check_mailbox(box_config):
    email_addr = box_config["email"]
    password = box_config["password"]
    if not password:
        log_message(f"Skipping sync for {email_addr} (password not configured).")
        return
        
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(email_addr, password)
        mail.select("inbox")
        
        # Search for unread emails (UNSEEN)
        status, response = mail.search(None, "UNSEEN")
        if status != "OK":
            mail.logout()
            return
            
        email_ids = response[0].split()
        log_message(f"Checking {email_addr}: found {len(email_ids)} unread emails.")
        
        for e_id in email_ids:
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            if status != "OK":
                continue
                
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = clean_header(msg["Subject"])
            from_header = clean_header(msg["From"])
            
            # Extract plain text body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode("utf-8", errors="ignore")
                        break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode("utf-8", errors="ignore")
                
            # Pattern matching Web3Forms submissions
            is_submission = "New Shop Registration" in subject or "New RepairBill Waitlist Signup" in subject
            is_reply = any(rep in subject.lower() for rep in ["re:", "fwd:"])
            
            if is_submission:
                log_message(f"Found Web3Forms signup submission: {subject}")
                fields = parse_body_fields(body)
                lead_email = fields.get("email") or fields.get("Email")
                if lead_email:
                    # Update status in CSV
                    if not update_lead_status(lead_email, "Trial"):
                        # If lead not present, add them as a direct signup
                        add_new_lead_to_csv(fields, source=box_config["source"])
                    # Mark email as read/seen in Hostinger mailbox
                    mail.store(e_id, "+FLAGS", "\\Seen")
                    log_message(f"Successfully processed and marked as seen: {lead_email}")
                    
            elif is_reply:
                log_message(f"Found customer reply: {subject}")
                # Try to extract the sender's email from From header
                match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", from_header)
                if match:
                    reply_email = match.group(0)
                    if update_lead_status(reply_email, "Replied"):
                        mail.store(e_id, "+FLAGS", "\\Seen")
                        log_message(f"Updated status to 'Replied' for: {reply_email}")
                        
        mail.close()
        mail.logout()
    except Exception as e:
        log_message(f"IMAP error for {email_addr}: {str(e)}")

if __name__ == "__main__":
    log_message("Starting Hostinger IMAP CRM Synchronizer sync run.")
    for config in MAILBOXES:
        check_mailbox(config)
    rebuild_crm_dashboard()
    log_message("Sync run completed successfully.")
