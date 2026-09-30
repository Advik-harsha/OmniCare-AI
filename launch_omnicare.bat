@echo off
setlocal enabledelayedexpansion
title OmniCare AI — Snapdragon X Elite Clinical Workstation

cd /d "%~dp0"

echo =====================================================================
echo   OmniCare AI — On-Device Clinical Diagnostic Workstation
echo   Qualcomm Snapdragon(R) AI Lab Build ^& Present Challenge 2026
echo   Target: Snapdragon X Elite (45 TOPS Qualcomm Hexagon NPU)
echo   Hardware Synergies: HP Poly Studio, HP Wolf Security, HP Smart Sense
echo   Privacy: Zero Cloud Egress ^| Local Enclave (DPDP Act Aligned)
echo =====================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH.
    echo Please install Python 3.10+ from https://www.python.org/ or Windows Store and re-run.
    pause
    exit /b 1
)

echo [1/3] Checking environment & dependencies...
if exist ".venv\Scripts\python.exe" (
    echo Using existing virtual environment in .venv
    set PYTHON_EXEC=.venv\Scripts\python.exe
) else (
    set PYTHON_EXEC=python
)

%PYTHON_EXEC% -m pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Pip install returned non-zero. Attempting backend/requirements.txt...
    %PYTHON_EXEC% -m pip install -q -r backend/requirements.txt
)

echo.
echo [2/3] Checking Execution Mode...
%PYTHON_EXEC% -c "import platform; print('Host Architecture:', platform.machine(), '| Processor:', platform.processor())"

echo.
echo [3/3] Starting OmniCare AI Diagnostic Workstation...
echo API server listening at http://localhost:8000
echo Clinical Cockpit UI at  http://localhost:8000/cockpit/
echo Offline Showcase at     showcase/index.html
echo Executive Pitch Deck at showcase/pitch-deck.html
echo.

start "" "http://localhost:8000/cockpit/"
%PYTHON_EXEC% -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
pause
