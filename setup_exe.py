"""
Build script to create standalone .exe file
Run: python setup_exe.py
"""

import os
import shutil
import subprocess
import sys

def clean_build():
    """Clean previous build files"""
    folders = ['build', 'dist', '__pycache__']
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✅ Removed {folder}")
    
    # Remove .spec files
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            os.remove(file)
            print(f"✅ Removed {file}")

def create_exe():
    """Create executable using PyInstaller"""
    
    print("\n" + "="*50)
    print("🚀 Building Restaurant Billing System Executable")
    print("="*50 + "\n")
    
    # Clean previous builds
    clean_build()
    
    # Create style.css if it doesn't exist
    if not os.path.exists('style.css'):
        print("⚠️ style.css not found, creating default...")
        with open('style.css', 'w') as f:
            f.write("""
QMainWindow { background-color: #FFFBDE; }
QLineEdit { border: 2px solid #129990; border-radius: 8px; padding: 8px; }
QPushButton { background-color: #129990; color: white; border-radius: 8px; padding: 8px; }
QPushButton:hover { background-color: #096B68; }
""")
    
    # PyInstaller command - FIXED
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name', 'RazaFoodBilling',
        '--windowed',
        '--onefile',
        '--add-data', f'style.css{os.pathsep}.',
        '--hidden-import', 'PyQt5',
        '--hidden-import', 'sqlite3',
        '--hidden-import', 'bcrypt',
        '--hidden-import', 'reportlab',
        '--hidden-import', 'pandas',
        '--hidden-import', 'openpyxl',
        'main.py'
    ]
    
    print("📦 Building executable...")
    print("⏳ This may take 2-3 minutes...\n")
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print("\n" + "="*50)
        print("✅ BUILD SUCCESSFUL!")
        print("="*50)
        print(f"\n📁 Executable location: {os.path.abspath('dist/RazaFoodBilling.exe')}")
        return True
    else:
        print("\n❌ Build failed! Trying alternative method...")
        return alternative_build()

def alternative_build():
    """Alternative build method without --add-data"""
    
    print("\n🔄 Trying alternative build method...")
    
    # Copy style.css to current directory for build
    if os.path.exists('style.css'):
        shutil.copy('style.css', 'style_copy.css')
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name', 'RazaFoodBilling',
        '--windowed',
        '--onefile',
        '--hidden-import', 'PyQt5',
        '--hidden-import', 'sqlite3',
        '--hidden-import', 'bcrypt',
        '--hidden-import', 'reportlab',
        '--hidden-import', 'pandas',
        '--hidden-import', 'openpyxl',
        'main.py'
    ]
    
    result = subprocess.run(cmd, capture_output=False)
    
    # Clean up
    if os.path.exists('style_copy.css'):
        os.remove('style_copy.css')
    
    if result.returncode == 0:
        print("\n✅ BUILD SUCCESSFUL with alternative method!")
        print(f"\n📁 Executable location: {os.path.abspath('dist/RazaFoodBilling.exe')}")
        return True
    
    return False

def create_portable_folder():
    """Create a portable folder with all necessary files"""
    
    portable_dir = "RazaFoodBilling_Portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    
    os.makedirs(portable_dir)
    
    # Copy exe
    exe_path = "dist/RazaFoodBilling.exe"
    if os.path.exists(exe_path):
        shutil.copy(exe_path, portable_dir)
    else:
        # Try to find exe in different location
        alt_path = "RazaFoodBilling.exe"
        if os.path.exists(alt_path):
            shutil.copy(alt_path, portable_dir)
    
    # Create necessary folders
    for folder in ['database', 'backups', 'receipts']:
        os.makedirs(os.path.join(portable_dir, folder), exist_ok=True)
    
    # Create run script
    run_script = """@echo off
start RazaFoodBilling.exe
"""
    with open(os.path.join(portable_dir, "RUN.bat"), "w") as f:
        f.write(run_script)
    
    # Create readme file
    readme_content = """========================================
    RAZA FOOD BILLING SYSTEM
========================================

📌 HOW TO RUN:
1. Double-click 'RazaFoodBilling.exe'
   OR
2. Double-click 'RUN.bat'

📌 FIRST TIME SETUP:
- The first run may take 5-10 seconds
- Database will be created automatically
- Default admin login: admin / admin123

📌 SYSTEM REQUIREMENTS:
- Windows 7 or higher
- No Python installation needed!

📌 KEYBOARD SHORTCUTS:
- ENTER = Print Bill
- Ctrl+N = New Order
- TAB = Next Field
- F1 = Help

📌 FOLDER STRUCTURE:
- database/ - contains all order data
- backups/ - automatic daily backups
- receipts/ - PDF copies of all bills

========================================
"""
    
    with open(os.path.join(portable_dir, "README.txt"), "w") as f:
        f.write(readme_content)
    
    print(f"\n📁 Portable folder created: {portable_dir}/")
    print("   Copy this folder to any computer and run RazaFoodBilling.exe")

if __name__ == "__main__":
    print("\n🔧 Restaurant Billing System - Executable Builder")
    print("="*50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # Create executable
    success = create_exe()
    
    if success:
        create_portable_folder()
        print("\n✨ Build Complete!")
        print("\n📋 To share with owner:")
        print("   1. Copy the 'RazaFoodBilling_Portable' folder")
        print("   2. Paste on owner's computer")
        print("   3. Double-click 'RazaFoodBilling.exe'")
    else:
        print("\n❌ Build failed. Trying one more method...")
        # Final attempt with simple command
        print("\n🔄 Running simple PyInstaller command...")
        os.system('pyinstaller --onefile --windowed --name "RazaFoodBilling" main.py')
        
        if os.path.exists("dist/RazaFoodBilling.exe"):
            print("\n✅ Build successful!")
            create_portable_folder()
        else:
            print("\n❌ Build failed. Please check:")
            print("   1. Make sure all files are in the correct folder")
            print("   2. Run: pip install pyinstaller")
            print("   3. Run: pyinstaller --onefile --windowed main.py")
    
    print("\nPress Enter to exit...")
    input()