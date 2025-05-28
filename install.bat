@echo off
echo NymNuker Setup
echo ===============

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Installing requirements...
python -m pip install -r requirements.txt

echo.
echo Setup complete! You can now run NymNuker.
echo.
echo To start the program, open start.bat
echo.

pause
