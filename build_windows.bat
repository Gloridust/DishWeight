@echo off
echo ====================================================
echo DishWeight System - Windows Build Script
echo ====================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo Python found, starting build process...
echo.

REM Run the build script
python build_windows.py

echo.
echo Build process completed.
echo Check the output above for any errors.
echo.
pause