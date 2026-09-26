param (
    [switch]$RunOnce,
    [switch]$VerifyOnly
)

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  OmniCare AI - Ralph Autonomous Task Runner" -ForegroundColor White
Write-Host "  Iterative loop with external state and git tracking" -ForegroundColor Yellow
Write-Host "=====================================================================" -ForegroundColor Cyan

$prdPath = "prd.json"
$progressFile = "progress.txt"

if (-not (Test-Path $prdPath)) {
    Write-Host "[ERROR] prd.json not found!" -ForegroundColor Red
    exit 1
}

$prd = Get-Content $prdPath -Raw | ConvertFrom-Json
Write-Host ""
Write-Host "Project: $($prd.project) v$($prd.version)" -ForegroundColor Green
Write-Host "Hardware Target: $($prd.hardware_target)" -ForegroundColor Gray
Write-Host "NPU: $($prd.npu)" -ForegroundColor Gray

$totalTasks = 0
$completedTasks = 0
$pendingTasks = @()

foreach ($phase in $prd.phases) {
    foreach ($task in $phase.tasks) {
        $totalTasks++
        if ($task.status -eq "completed") {
            $completedTasks++
        } else {
            $pendingTasks += [PSCustomObject]@{
                Phase = $phase.name
                Id = $task.id
                Title = $task.title
                Status = $task.status
            }
        }
    }
}

Write-Host ""
Write-Host "Tasks Completed: $completedTasks / $totalTasks" -ForegroundColor Cyan

if ($VerifyOnly) {
    Write-Host ""
    Write-Host "[VERIFY MODE] Checking test suite..." -ForegroundColor Yellow
    if (Test-Path "backend/test_endpoints.py") {
        python backend/test_endpoints.py
    } else {
        Write-Host "backend/test_endpoints.py will be executed in Phase 6." -ForegroundColor Gray
    }
    exit 0
}

if ($pendingTasks.Count -eq 0) {
    Write-Host ""
    Write-Host "[SUCCESS] All tasks in prd.json are marked COMPLETED! Ready for submission." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "Next Pending Tasks in PRD Queue:" -ForegroundColor Yellow
foreach ($t in ($pendingTasks | Select-Object -First 3)) {
    Write-Host "  - [$($t.Id)] $($t.Title) (Phase: $($t.Phase))" -ForegroundColor White
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logEntry = "[$timestamp] Ralph iteration checked. Completed: $completedTasks/$totalTasks. Next up: $($pendingTasks[0].Id) - $($pendingTasks[0].Title)"
Add-Content -Path $progressFile -Value $logEntry

Write-Host ""
Write-Host "Logged iteration to $progressFile." -ForegroundColor Green
Write-Host "Ralph loop runner ready." -ForegroundColor Cyan
