@echo off
REM Product Image Organizer - Build Script for Windows
REM This script builds the application into a standalone EXE file

echo ================================================
echo   Product Image Organizer - Build Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Python found. Installing PyInstaller...
pip install pyinstaller --quiet
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo [2/3] PyInstaller installed. Building application...
python -m PyInstaller --onefile --noconsole product_image_organizer.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo [3/3] Build completed successfully!
echo.
echo ================================================
echo   EXE created: dist\product_image_organizer.exe
echo ================================================
echo.
echo You can now:
echo   1. Double-click the EXE to run the application
echo   2. Move it anywhere on your computer
echo   3. Share it with others (no Python needed)
echo.
pause
