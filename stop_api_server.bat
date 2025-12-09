@echo off
chcp 65001 >nul 2>&1
REM ============================================
REM AGV API Server Stop Script (Windows)
REM ============================================

echo ============================================
echo Stopping AGV API Server...
echo ============================================
echo.

REM Find running Python/uvicorn processes
echo [SEARCH] Searching for Python processes...
echo.

tasklist /FI "IMAGENAME eq python.exe" /FO TABLE 2>nul | findstr "python.exe" >nul

if %ERRORLEVEL% EQU 0 (
    echo [FOUND] Found the following Python processes:
    echo.
    tasklist /FI "IMAGENAME eq python.exe" /FO TABLE
    echo.

    REM Ask for confirmation to stop all Python processes
    set /p "confirm=Do you want to stop all Python processes? (y/n): "

    if /i "%confirm%"=="y" (
        echo.
        echo [EXECUTE] Stopping Python processes...
        taskkill /F /IM python.exe >nul 2>&1

        if %ERRORLEVEL% EQU 0 (
            echo [SUCCESS] Python processes stopped
        ) else (
            echo [FAILED] Cannot stop processes, administrator privileges may be required
        )
    ) else (
        echo [CANCEL] Operation cancelled
    )
) else (
    echo [INFO] No running Python processes found
)

echo.
echo ============================================
echo Operation completed
echo ============================================
pause
