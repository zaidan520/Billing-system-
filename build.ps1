# PowerShell Build Script for Raza Food Billing System

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BUILDING RAZA FOOD BILLING SYSTEM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set working directory
Set-Location "C:\Users\WitChER.PRIME\Documents\Restaurat Billing"

# Create style.css if missing
if (-not (Test-Path "style.css")) {
    Write-Host "Creating style.css..." -ForegroundColor Yellow
    @"
QMainWindow { background-color: #FFFBDE; }
QLineEdit { border: 2px solid #129990; border-radius: 8px; padding: 8px; }
QPushButton { background-color: #129990; color: white; border-radius: 8px; padding: 8px; }
QPushButton:hover { background-color: #096B68; }
"@ | Out-File -FilePath "style.css" -Encoding utf8
    Write-Host "✅ style.css created" -ForegroundColor Green
}

# Install PyInstaller
Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
python -m pip install pyinstaller --quiet

# Build executable
Write-Host "Building executable (this may take 2-3 minutes)..." -ForegroundColor Yellow
python -m PyInstaller --onefile --windowed --name "RazaFoodBilling" main.py

# Check if build succeeded
if (Test-Path "dist\RazaFoodBilling.exe") {
    Write-Host ""
    Write-Host "✅ BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "📁 Executable: dist\RazaFoodBilling.exe" -ForegroundColor White
    Write-Host ""
    
    # Copy to desktop
    Copy-Item "dist\RazaFoodBilling.exe" -Destination "$env:USERPROFILE\Desktop\" -Force
    Write-Host "✅ Copied to Desktop!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 You can now run RazaFoodBilling.exe from your desktop" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ BUILD FAILED!" -ForegroundColor Red
    Write-Host "Please run this command manually:" -ForegroundColor Yellow
    Write-Host "python -m PyInstaller --onefile --windowed main.py" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")