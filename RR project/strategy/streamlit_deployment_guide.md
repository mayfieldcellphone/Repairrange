# Step-by-Step Deployment Guide: Streamlit Community Cloud (Option B)

This guide provides instructions to deploy your local **RepairRange CRM & Lead Sourcing Hub** to the web securely and for free.

---

## Prerequisites
1. A free [GitHub account](https://github.com).
2. Git installed on your local computer.
3. Your local files are ready (we have already created `requirements.txt` and `.gitignore` to support this deployment).

---

## Step 1: Initialize Git & Push to GitHub

1. Open your terminal or command prompt in your project root directory.
2. Initialize Git, add all files, and commit them:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of RepairRange Hub"
   ```
   *(Note: The `.gitignore` file we created will automatically prevent your secret `.env` file or background files from being uploaded to GitHub.)*

3. Create a **Private Repository** on GitHub:
   * Go to [github.com/new](https://github.com/new).
   * Name your repository (e.g., `repairrange-crm`).
   * Choose **Private** (highly recommended so your leads and logic remain confidential).
   * Do NOT check "Add a README" or ".gitignore" (since we already have them).
   * Click **Create repository**.

4. Link your local project to GitHub and push:
   ```bash
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/repairrange-crm.git
   git branch -M main
   git push -u origin main
   ```

---

## Step 2: Set up Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and click **"Connect with GitHub"** or sign up.
2. Once logged in, click the **"Create app"** button in the top right.
3. Fill in the deployment details:
   * **Repository:** `YOUR_GITHUB_USERNAME/repairrange-crm`
   * **Branch:** `main`
   * **Main file path:** `app.py`
   * **App URL:** Customize your public subdomain (e.g., `repairrange-crm.streamlit.app`).

---

## Step 3: Configure Your Secrets (.env credentials)

Because we excluded your `.env` file from GitHub for security, you must paste your credentials into Streamlit's secure vault:

1. On the Streamlit deployment page, click **"Advanced settings..."** before deploying, or click **"Settings" -> "Secrets"** in your app's dashboard.
2. Open your local `.env` file, copy all lines, and paste them directly into the **Secrets** textbox in the exact same format:
   ```toml
   # Copy and paste from your local .env file
   GOOGLE_PLACES_API_KEY = "your-api-key"
   SENDER_EMAIL = "your-email"
   SENDER_PASSWORD = "your-password"
   IMAP_SERVER = "imap.hostinger.com"
   SMTP_SERVER = "smtp.hostinger.com"
   # ...and any other .env keys
   ```
3. Click **"Save"**. Streamlit will automatically inject these as secure environment variables, allowing the backend scripts to run flawlessly.

---

## Step 4: Launch and Access Your App!

1. Click **"Deploy!"**.
2. Streamlit will boot up a secure container, install the packages listed in `requirements.txt`, and render your app. This takes about 1-2 minutes on the first run.
3. Your app is now live!

### How to Keep it Private
By default, because your GitHub repository is **Private**, Streamlit restricts access to your app. Only **you** (when logged into your Streamlit account) can view or interact with it. 

If you want to share it with virtual assistants or other members of your team:
1. Open your Streamlit App.
2. Click **"Share"** in the top-right corner.
3. Enter their email address to invite them securely.
