@echo off
title Building Raza Food Billing System
echo ========================================
echo   BUILDING EXECUTABLE FILE
echo ========================================
echo.

echo Creating style.css if missing...
if not exist style.css (
    echo QMainWindow { background-color: #FFFBDE; } > style.css
    echo QPushButton { background-color: #129990; color: white; border-radius: 8px; } >> style.css
    echo QPushButton:hover { background-color: #096B68; } >> style.css
    echo ✅ Created style.css
)

echo.
echo Installing PyInstaller...
python -m pip install pyinstaller --quiet

echo.
echo Building executable...
echo This may take 2-3 minutes...
echo.

python -m PyInstaller --onefile --windowed --name "RazaFoodBilling" main.py

echo.
if exist "dist\RazaFoodBilling.exe" (
    echo ========================================
    echo   ✅ BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo 📁 Executable: dist\RazaFoodBilling.exe
    echo.
    echo Copying to desktop...
    copy "dist\RazaFoodBilling.exe" "%USERPROFILE%\Desktop\" >nul 2>&1
    echo ✅ Copied to Desktop!
    echo.
    echo 🚀 You can now run RazaFoodBilling.exe from your desktop
) else (
    echo ========================================
    echo   ❌ BUILD FAILED!
    echo ========================================
    echo.
    echo Trying alternative method...
    echo.
    
    python -m PyInstaller --onefile --windowed --name "RazaFoodBilling" --hidden-import PyQt5 --hidden-import sqlite3 main.py
    
    if exist "dist\RazaFoodBilling.exe" (
        echo ✅ Build successful on second attempt!
        copy "dist\RazaFoodBilling.exe" "%USERPROFILE%\Desktop\" >nul 2>&1
    ) else (
        echo ❌ Still failed. Please run this command manually:
        echo python -m PyInstaller --onefile --windowed main.py
    )
)

echo.
echo ========================================
echo.
pause