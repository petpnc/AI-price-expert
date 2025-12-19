@echo off
REM ValueAI - Quick Startup Script for Windows

echo.
echo ========================================
echo   ValueAI - Starting...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if dependencies are installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Check if API key is configured
findstr "your-google-api-key-here" .streamlit\secrets.toml >nul 2>&1
if not errorlevel 1 (
    echo.
    echo ========================================
    echo   WARNING: API key not configured!
    echo ========================================
    echo.
    echo Please edit .streamlit\secrets.toml
    echo and add your Google API key
    echo.
    pause
)

REM Start the app
echo.
echo ========================================
echo   Starting ValueAI...
echo ========================================
echo.
echo App will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop
echo.

streamlit run app.py

pause
