"""
Build script - Run this with: python run_build.py
"""

import os
import subprocess
import sys
import shutil

def main():
    print("\n" + "="*50)
    print("  RAZA FOOD BILLING - BUILD EXECUTABLE")
    print("="*50 + "\n")
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create style.css if missing
    if not os.path.exists('style.css'):
        print("📝 Creating style.css...")
        with open('style.css', 'w') as f:
            f.write("""
QMainWindow { background-color: #FFFBDE; }
QLineEdit { border: 2px solid #129990; border-radius: 8px; padding: 8px; }
QPushButton { background-color: #129990; color: white; border-radius: 8px; padding: 8px; }
QPushButton:hover { background-color: #096B68; }
""")
        print("✅ style.css created\n")
    
    # Install PyInstaller
    print("📦 Installing PyInstaller...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller', '--quiet'])
    
    # Build executable
    print("\n🔧 Building executable (this may take 2-3 minutes)...\n")
    result = subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', 'RazaFoodBilling',
        'main.py'
    ])
    
    # Check result
    if os.path.exists('dist/RazaFoodBilling.exe'):
        print("\n" + "="*50)
        print("✅ BUILD SUCCESSFUL!")
        print("="*50)
        print(f"\n📁 Location: {os.path.abspath('dist/RazaFoodBilling.exe')}")
        
        # Copy to desktop
        desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        shutil.copy('dist/RazaFoodBilling.exe', desktop)
        print(f"✅ Copied to: {desktop}\\RazaFoodBilling.exe")
        
        print("\n🚀 You can now double-click RazaFoodBilling.exe to run!")
    else:
        print("\n❌ BUILD FAILED!")
        print("\nTry running this command manually:")
        print(f'{sys.executable} -m PyInstaller --onefile --windowed main.py')
    
    print("\nPress Enter to exit...")
    input()

if __name__ == '__main__':
    main()