# JARVIS Full Stack Starter
# Run this script to start both backend and frontend

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "          JARVIS AI SYSTEM LAUNCHER            " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Kill existing processes on ports 5000 and 8080
Write-Host "[1/4] Stopping existing servers..." -ForegroundColor Yellow
Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*jarvis*" } | Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

# Start Backend
Write-Host "[2/4] Starting JARVIS Backend (Flask)..." -ForegroundColor Green
$backendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\JARVIS\jarvis-ai; python api_server.py" -PassThru

Start-Sleep -Seconds 3

# Start Frontend
Write-Host "[3/4] Starting JARVIS Frontend (React)..." -ForegroundColor Green
$frontendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\JARVIS\jarvis-frontend; npm run dev" -PassThru

Start-Sleep -Seconds 5

# Open browser
Write-Host "[4/4] Opening JARVIS interface..." -ForegroundColor Green
Start-Process "http://localhost:8080"

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "          JARVIS SYSTEM STARTED!               " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:5000" -ForegroundColor White
Write-Host "Frontend: http://localhost:8080" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit this launcher..." -ForegroundColor Gray
Write-Host "(The servers will continue running)" -ForegroundColor Gray

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
