@echo off
REM ==================== JARVIS Python Windows Startup Setup ====================
REM This script adds JARVIS to Windows startup

echo.
echo ==========================================
echo    JARVIS Python Auto-Start Setup
echo ==========================================
echo.

REM Get startup folder path
set "StartupFolder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

REM Copy VBS script to startup folder
echo Installing JARVIS to Windows Startup...
copy /Y "%~dp0jarvis-python-silent.vbs" "%StartupFolder%\JARVIS-Python.vbs"

if %errorlevel% == 0 (
    echo.
    echo ==========================================
    echo    SUCCESS! JARVIS Auto-Start Enabled
    echo ==========================================
    echo.
    echo JARVIS will now start automatically when Windows boots
    echo.
    echo To disable auto-start:
    echo 1. Press Win+R
    echo 2. Type: shell:startup
    echo 3. Delete JARVIS-Python.vbs
    echo.
) else (
    echo.
    echo ERROR: Failed to install auto-start
    echo Please run this script as Administrator
    echo.
)

pause
