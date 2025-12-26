@echo off
echo ========================================
echo Starting JARVIS Full Stack Application
echo ========================================
echo.

echo Starting Flask Backend Server...
start "JARVIS Backend" cmd /k "cd /d %~dp0jarvis-ai && python api_server.py"

timeout /t 3 /nobreak >nul

echo Starting React Frontend...
start "JARVIS Frontend" cmd /k "cd /d %~dp0jarvis-frontend && npm run dev"

echo.
echo ========================================
echo Both servers are starting...
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:5173
echo ========================================
echo.
echo Press any key to stop all servers...
pause >nul

taskkill /FI "WindowTitle eq JARVIS Backend*" /T /F
taskkill /FI "WindowTitle eq JARVIS Frontend*" /T /F

echo.
echo All servers stopped.
pause
