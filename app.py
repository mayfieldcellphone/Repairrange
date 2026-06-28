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
    "🛒 Store Catalog Sync"
]
page = st.sidebar.radio("Navigation Menu", menu_options)

# Helper function to run sub-processes with console output
def run_script_live(script_name, args=[]):
    script_path = os.path.join(ROOT_DIR, script_name)
    if not os.path.exists(script_path):
        st.error(f"Script file not found: {script_name}")
        return
    
    st.info(f"🚀 Running: `{script_name}`")
    try:
        result = subprocess.run([sys.executable, script_path] + args, capture_output=True, text=True)
        if result.returncode == 0:
            st.success(result.stdout)
        else:
            st.error(result.stderr)
    except Exception as e:
        st.error(f"Failed to execute script: {str(e)}")

# Load data helper
def load_data():
    if not os.path.exists(CSV_PATH): return pd.DataFrame()
    return pd.read_csv(CSV_PATH)

# --- PAGE ROUTING ---

if page == "📊 Dashboard & Pipeline":
    st.title("📊 Pipeline Analytics")
    df = load_data()
    if not df.empty:
        st.write(f"Total Leads: {len(df)}")
        st.bar_chart(df['Status'].value_counts())

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

st.sidebar.markdown("---")
st.sidebar.info("v1.3.0 | Master Data Integrated")
