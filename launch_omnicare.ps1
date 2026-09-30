# OmniCare AI — PowerShell Launcher
# Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026

Set-Location $PSScriptRoot

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  OmniCare AI — On-Device Clinical Diagnostic Workstation" -ForegroundColor White
Write-Host "  Target Hardware: Snapdragon X Elite (45 TOPS Qualcomm Hexagon NPU)" -ForegroundColor Yellow
Write-Host "  Privacy: Zero Cloud Egress • Local Enclave (DPDP Act Aligned)" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[ERROR] Python not found in PATH. Please install Python 3.10+ from python.org." -ForegroundColor Red
    exit 1
}

Write-Host "`n[1/3] Verifying Python requirements..." -ForegroundColor Gray
if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "Using virtual environment (.venv)..." -ForegroundColor DarkGray
    & .venv\Scripts\python.exe -m pip install -q -r requirements.txt
    $py = ".venv\Scripts\python.exe"
} else {
    python -m pip install -q -r requirements.txt
    $py = "python"
}

Write-Host "`n[2/3] Checking Execution Mode..." -ForegroundColor Gray
& $py -c "import platform; print('Host Architecture: ' + platform.machine() + ' | Processor: ' + platform.processor())"

Write-Host "`n[3/3] Starting OmniCare AI Diagnostic Workstation on http://localhost:8000..." -ForegroundColor Cyan
Write-Host "Opening Clinical Cockpit UI at http://localhost:8000/cockpit/..." -ForegroundColor Green
Start-Process "http://localhost:8000/cockpit/"

& $py -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
