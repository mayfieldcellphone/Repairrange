# RepairRange Outreach Campaign: Execution & Verification Guide

This guide describes how to run and verify the RepairRange.io email outreach campaign. It includes the quality check (QC) process, exact commands for sending emails using the Gmail API integration, and the mandatory post-send delivery verification workflow.

---

## 1. Quality Check (QC) & Verification Checklist

Before sending any emails, the following checks **must** be performed for every lead:

- [ ] **Valid Domain/Email**: Verify that the email address is syntactically valid and active.
- [ ] **Localized Subject & City**: Confirm that the subject line contains the correct city (e.g., `Sydney` for Sydney shops, `Melbourne` for Melbourne shops).
- [ ] **Proper Greeting Fallback**: Check that the greeting addresses the `[Shop Name] Team` instead of a blank or broken first name variable.
- [ ] **Working Landing Page Link**: Ensure that the link `https://www.repairrange.io/list-your-shop.html` is fully functional and loading correctly.
- [ ] **No HTML Format Issues**: Since we are using plain-text format for higher deliverability (to avoid spam folders), ensure there are no unescaped HTML tags in the body.

---

## 2. Sending Emails via Gmail API (Using ACCIO CLI)

Your connected Gmail account is **`support@selfrepairkit.com.au`**. We can utilize the `send_gmail_message` tool to programmatically send these personalized emails directly from Gmail.

### Exact CLI Tool Call Format
For each lead, we run the following command. (The message body should be plain-text format for maximum deliverability).

```bash
accio-mcp-cli call send_gmail_message --json '{
  "user_google_email": "support@selfrepairkit.com.au",
  "to": "Ask@SydneyCBDrepairCentre.com.au",
  "subject": "Free listing on RepairRange.io — Sydney repair pricing guide",
  "body": "Hi Sydney CBD Repair Centre Team,\n\nI run RepairRange.io — an independent phone repair pricing guide covering Sydney. We\u0027re currently adding verified local shop listings, and I\u0027d love to include Sydney CBD Repair Centre.\n\nYour first month is completely free — you can view our plans and apply directly here:\n👉 https://www.repairrange.io/list-your-shop.html\n\nWhat you get: Your shop featured prominently on our Sydney pricing page, putting you directly in front of local customers actively searching for repair costs. There are no commissions and no per-click charges — just a simple, flat listing fee starting at $29/quarter.\n\nBest regards,\n\nKhalil\nRepairRange / Mayfield Phone Repair, Newcastle",
  "body_format": "text"
}'
```

---

## 3. Post-Send Delivery Verification Workflow (Mandatory)

To protect the sender reputation of `support@selfrepairkit.com.au` and ensure campaign accuracy, you **MUST** run the delivery status verification after sending a batch of emails.

### 3.1 Wait Time
Wait **5 to 10 seconds** after sending an email to allow mail servers to attempt routing and generate bounce-backs.

### 3.2 Run Bounce Search Command
Execute this optimized search query to check for any delivery failures:

```bash
accio-mcp-cli call search_gmail_messages --json '{
  "user_google_email": "support@selfrepairkit.com.au",
  "query": "from:mailer-daemon@googlemail.com (subject:\"Delivery Status Notification\" OR subject:\"找不到地址\" OR subject:\"Address not found\") newer_than:1d",
  "page_size": 5
}'
```

### 3.3 Evaluating Bounce Results
1. **No relevant bounce returned**: The email reached the destination mail server successfully. Mark status as **`Delivered`**.
2. **Bounce found**: 
   - Inspect the returned bounce body to extract the specific failed recipient email.
   - Mark the lead status in the tracking sheet as **`Bounced (Invalid Address)`**.
   - If a website/phone number is available, attempt to find a correct email address, or fall back to contact form submission.

---

## 4. Best Practices for High Deliverability

1. **Daily Send Limits**: Do **not** send all 25 emails at once. Send them in batches of **5-10 per day** to avoid triggering automated spam algorithms on new Gmail threads.
2. **No Tracking Pixels**: Do not attach tracking pixels or large image signatures in the initial cold outreach email. Simple plain-text emails receive up to **2x higher response rates** because they look like genuine personal emails.
3. **Sender Persona**: The signature "Khalil RepairRange / Mayfield Phone Repair, Newcastle" is your strongest tool. It establishes that you are a peer in the industry, not an aggressive third-party SaaS solicitor. Maintain this credibility by replying promptly and personally to any inquiries.
