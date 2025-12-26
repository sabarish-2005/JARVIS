@echo off
title JARVIS - Full System
color 0A

echo ================================================
echo          JARVIS AI SYSTEM LAUNCHER
echo ================================================
echo.

:: Kill any existing processes on ports
echo Stopping any existing servers...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1

timeout /t 2 /nobreak >nul

:: Start Backend
echo.
echo [1/2] Starting JARVIS Backend Server...
cd /d "%~dp0jarvis-ai"
start "JARVIS Backend" cmd /k "python api_server.py"

:: Wait for backend to initialize
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

:: Start Frontend
echo.
echo [2/2] Starting JARVIS Frontend...
cd /d "%~dp0jarvis-frontend"
start "JARVIS Frontend" cmd /k "npm run dev"

:: Wait for frontend
timeout /t 3 /nobreak >nul

echo.
echo ================================================
echo          JARVIS SYSTEM STARTED!
echo ================================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8080
echo.
echo Press any key to open the JARVIS interface...
pause >nul

:: Open browser
start http://localhost:8080

echo.
echo JARVIS is running. Close this window to keep servers running.
echo To stop: Close the Backend and Frontend terminal windows.
pause
