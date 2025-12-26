@echo off
REM ==================== JARVIS API - START SCRIPT ====================
REM This script starts the JARVIS API server for React frontend integration

echo.
echo ========================================================
echo  JARVIS API SERVER STARTUP
echo ========================================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_jarvis.py first
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\Activate.ps1

echo.
echo Installing API dependencies...
pip install flask flask-cors > nul 2>&1

if %errorlevel% neq 0 (
    echo Installing from requirements file...
    pip install -r requirements-api.txt
)

echo.
echo ========================================================
echo Starting JARVIS API Server...
echo ========================================================
echo.
echo API Server: http://localhost:5000
echo API Docs:   http://localhost:5000/api/docs
echo React Port: 3000 (use http://localhost:3000)
echo.
echo Press CTRL+C to stop the server
echo.

python api_server.py

pause
