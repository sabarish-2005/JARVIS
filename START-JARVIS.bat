@echo off
title JARVIS AI System
color 0B

echo ================================================
echo           JARVIS AI SYSTEM LAUNCHER
echo ================================================
echo.

:: Kill existing processes
echo [1/4] Stopping existing servers...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

:: Start Backend in new window
echo [2/4] Starting JARVIS Backend...
start "JARVIS Backend" cmd /k "cd /d D:\JARVIS\jarvis-ai && python api_server.py"
timeout /t 3 /nobreak >nul

:: Start Frontend in new window
echo [3/4] Starting JARVIS Frontend...
start "JARVIS Frontend" cmd /k "cd /d D:\JARVIS\jarvis-frontend && npm run dev"
timeout /t 5 /nobreak >nul

:: Open browser
echo [4/4] Opening JARVIS interface...
start http://localhost:8080

echo.
echo ================================================
echo           JARVIS SYSTEM STARTED!
echo ================================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8080
echo.
echo Press any key to exit launcher...
echo (Servers will continue running)
pause >nul
