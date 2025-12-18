@echo off
REM Quick start script for RAG Knowledge Base

echo ========================================
echo  RAG Knowledge Base - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    exit /b 1
)

REM Check if .env file exists
if not exist ". env" (
    echo [WARNING] .env file not found!
    echo.
    echo Please create a .env file with your Google API key:
    echo GOOGLE_API_KEY=your_api_key_here
    echo.
    echo Get your free API key from:
    echo https://makersuite.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/3] Checking dependencies...
pip list | findstr streamlit >nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo [3/3] Starting Streamlit app...
echo.
echo ========================================
echo  App will open in your browser at:
echo  http://localhost:8501
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py
