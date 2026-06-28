#!/bin/bash
echo "====================================================================="
echo "   🔧 REPAIRRANGE - COLD OUTREACH & LEAD CRM DASHBOARD SYSTEM 🔧"
echo "====================================================================="
echo ""
echo "Checking environment dependencies..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "[INFO] Streamlit is not installed. Installing dependencies now..."
    pip3 install streamlit pandas
else
    echo "[OK] All dependencies satisfied!"
fi
echo ""
echo "Starting web app on local port 8501..."
echo ""
streamlit run app.py
