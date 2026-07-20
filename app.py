import streamlit as st
import pandas as pd
import os
import subprocess
import sys
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="RepairRange Hub",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(ROOT_DIR, "RR project", "leads", "outreach_schedule_june_2026.csv")
LOG_PATH = os.path.join(ROOT_DIR, "RR project", "strategy", "outreach_log.txt")
CATALOG_PATH = os.path.join(ROOT_DIR, "selfrepairkit", "catalog.json")
MASTER_EXCEL = os.path.join(ROOT_DIR, "SelfRepairKit-Master-Product-Database.xlsx")

# Sidebar
st.sidebar.title("🔧 RepairRange Hub")
menu_options = [
    "📊 Dashboard & Pipeline", 
    "🗃️ CRM Lead Manager", 
    "🛰️ Sourcing Hub", 
    "✉️ Email & Sync Control", 
    "🛒 Store Catalog Sync",
    "🔍 SEO Health Monitor",
    "⚙️ System Terminal"
]
page = st.sidebar.radio("Navigation Menu", menu_options)

# --- UI STYLING ---
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
    }
    .status-card {
        padding: 20px;
        border-radius: 12px;
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# --- PAGE ROUTING ---

if page == "📊 Dashboard & Pipeline":
    st.title("📊 Business Dashboard")
    
    # Live Site Status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="status-card"><b>RepairBill.shop</b><br><span style="color:green">● Online</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="status-card"><b>PDFRange.com</b><br><span style="color:green">● Online</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="status-card"><b>Mayfield Repair</b><br><span style="color:green">● Online</span></div>', unsafe_allow_html=True)

    df = load_data()
    if not df.empty:
        st.write(f"Total Leads: {len(df)}")
        st.bar_chart(df['Status'].value_counts())

elif page == "⚙️ System Terminal":
    st.title("⚙️ System Terminal")
    st.warning("⚠️ Critical: Execution of shell commands directly on the server.")
    
    cmd = st.text_input("Enter Shell Command")
    if st.button("Run Command"):
        if cmd:
            try:
                # Use a simple subprocess run for direct commands
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                st.code(result.stdout + "\n" + result.stderr)
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
    
    st.markdown("---")
    st.subheader("Common Fixes")
    if st.button("Unlock SSH (Unban All)"):
        try:
            subprocess.run("fail2ban-client unban --all", shell=True)
            st.success("Unbanned all IPs.")
        except:
            st.error("Fail2Ban command failed.")
    
    if st.button("Restart Web Server"):
        subprocess.run("systemctl restart nginx", shell=True)
        st.info("Nginx restarted.")

elif page == "🗃️ CRM Lead Manager":
    st.title("🗃️ Lead Manager")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Sync Cloud Leads", type="primary", use_container_width=True, help="Fetch new shop listings from Google Sheets"):
            run_script_live("sync_web_leads.py")
            st.rerun()
            
    df = load_data()
    if not df.empty:
        st.data_editor(df, use_container_width=True)

elif page == "🛰️ Sourcing Hub":
    st.title("🛰️ Lead Sourcing")
    city = st.text_input("Target City")
    if st.button("Start Sourcing"):
        st.info(f"Sourcing for {city}...")

elif page == "✉️ Email & Sync Control":
    st.title("✉️ Email Control")
    if st.button("Send Batch"):
        st.info("Sending emails...")

elif page == "🛒 Store Catalog Sync":
    st.title("🛒 Store Catalog Sync")
    st.subheader("Update Website from Master Database")
    
    col_excel, col_sheet = st.columns(2)
    
    with col_excel:
        st.markdown("### 📑 Local Master Excel")
        st.markdown("Synchronize using the local `SelfRepairKit-Master-Product-Database.xlsx` file.")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 Push to Website", type="primary", use_container_width=True, help="Update website using Excel prices"):
                run_script_live("sync_master_excel.py")
                st.rerun()
        with col_btn2:
            if st.button("📥 Pull from Website", use_container_width=True, help="Update Excel using Website prices"):
                run_script_live("back_sync_excel.py")
                st.rerun()
            
    with col_sheet:
        st.markdown("### ☁️ Google Sheet (Legacy)")
        st.markdown("Sync using the cloud-based spreadsheet.")
        sheet_id = st.text_input("Google Sheet ID", value="1TZ4wELPwdl__5Rmftuavzi-gNE904YAkbTJCZO1p-tg")
        if st.button("🔄 Sync with Cloud Sheet", use_container_width=True):
            st.info("Reading from Google Sheet...")
            # Future expansion for direct sheet parsing
    
    st.markdown("---")
    if os.path.exists(CATALOG_PATH):
        with st.expander("🔍 View Live Website Catalog.json"):
            with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
                st.json(json.load(f))

elif page == "🔍 SEO Health Monitor":
    st.title("🔍 SEO Health Monitor")
    st.subheader("Monitoring: repairbill.shop, pdfrange.com, mayfieldphonerepair.com.au")
    
    if st.button("🚀 Run Health Check Now"):
        st.info("Scanning domains for status, meta tags, and SSL expiry...")
        
        script_path = os.path.join(ROOT_DIR, "seo_monitor.py")
        try:
            result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for item in data:
                    with st.expander(f"🌐 {item['url']}", expanded=True):
                        col1, col2 = st.columns(2)
                        col1.write(f"**Status:** {item['status']}")
                        col1.write(f"**SSL Expiry:** {item['ssl_expiry']}")
                        col2.write(f"**Title:** {item['title']}")
                        col2.write(f"**Description:** {item['description']}")
                        
                        if item['title'] == "Missing" or item['description'] == "Missing":
                            st.warning("⚠️ SEO Meta Tags are incomplete!")
                        else:
                            st.success("✅ SEO Meta Tags are present.")
            else:
                st.error(f"Error running monitor: {result.stderr}")
        except Exception as e:
            st.error(f"Failed to execute SEO monitor: {str(e)}")

st.sidebar.markdown("---")
st.sidebar.info("v1.3.0 | Master Data Integrated")
