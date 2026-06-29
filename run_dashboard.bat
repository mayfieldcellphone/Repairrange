@echo off
title RepairRange CRM & Lead Sourcing Hub
echo =====================================================================
echo    🔧 REPAIRRANGE - COLD OUTREACH & LEAD CRM DASHBOARD SYSTEM 🔧
echo =====================================================================
echo.
echo Checking environment dependencies...
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Streamlit is not installed. Installing dependencies now...
    pip install streamlit pandas
) else (
    echo [OK] All dependencies satisfied!
)
echo.
echo Starting web app on local port 8501...
echo.
streamlit run app.py
pause
