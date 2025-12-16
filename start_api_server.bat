@echo off
chcp 65001 >nul 2>&1
REM ============================================
REM AGV API Server Start Script (Windows)
REM ============================================

echo ============================================
echo Starting AGV API Server...
echo ============================================
echo.

REM Change to script directory
cd /d "%~dp0"
if errorlevel 1 (
    echo [ERROR] Failed to change directory
    pause
    exit /b 1
)

REM Check virtual environment
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Virtual environment detected, activating...
    call venv\Scripts\activate.bat
    echo.
)

REM Display Python version
echo [INFO] Python version:
python --version 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)
echo.

REM Start FastAPI Server (Development mode)
echo [START] Starting FastAPI Server...
echo [MODE] Development mode (auto-reload enabled)
echo [HOST] Binding to all interfaces (0.0.0.0)
echo [URL] http://localhost:8000
echo [URL] http://192.168.12.99:8000
echo [DOCS] http://localhost:8000/docs
echo [DOCS] http://192.168.12.99:8000/docs
echo.
echo [TIP] Press Ctrl+C to stop the server
echo ============================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

REM Server stopped
echo.
echo ============================================
echo AGV API Server stopped
echo ============================================
pause
