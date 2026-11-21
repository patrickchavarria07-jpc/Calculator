@echo off
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
    py -3 calculator.py
    if errorlevel 1 pause
    exit /b
)
python --version >nul 2>nul
if errorlevel 1 (
    echo Python is not installed or is not available on PATH.
    echo This calculator requires Python with Tkinter, but no pip packages.
    pause
    exit /b 1
)
python calculator.py
if errorlevel 1 pause
