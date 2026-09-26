# OmniCare AI — PowerShell Launcher
# Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  OmniCare AI — On-Device Clinical Diagnostic Workstation" -ForegroundColor White
Write-Host "  Hardware: Snapdragon X Elite (45 TOPS Qualcomm Hexagon NPU)" -ForegroundColor Yellow
Write-Host "  Compliance: India DPDP Act 2023 (100% Zero Cloud Egress)" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[ERROR] Python not found in PATH. Please install Python 3.10+." -ForegroundColor Red
    exit 1
}

Write-Host "`n[1/2] Verifying Python requirements..." -ForegroundColor Gray
python -m pip install -q -r backend/requirements.txt

Write-Host "`n[2/2] Starting OmniCare AI Diagnostic Workstation on http://localhost:8000..." -ForegroundColor Cyan
Start-Process "http://localhost:8000"

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
