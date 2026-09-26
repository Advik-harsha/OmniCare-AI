@echo off
title OmniCare AI — Snapdragon X Elite Clinical Workstation
echo =====================================================================
echo   OmniCare AI — On-Device Clinical Diagnostic Workstation
echo   Qualcomm Snapdragon(R) AI Lab Build ^& Present Challenge 2026
echo   Target: Snapdragon X Elite (45 TOPS Qualcomm Hexagon NPU)
echo   Hardware Synergies: HP Poly Studio, HP Wolf Security, HP Smart Sense
echo =====================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH. Please install Python 3.10+ and re-run.
    pause
    exit /b 1
)

echo [1/2] Checking Python dependencies...
python -m pip install -q -r backend/requirements.txt

echo.
echo [2/2] Launching OmniCare AI FastAPI Diagnostic Engine...
echo Server starting at http://localhost:8000
echo Offline Showcase available at showcase/index.html
echo.

start "" "http://localhost:8000"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
pause
