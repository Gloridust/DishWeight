#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows EXE Build Script
Automated packaging script for DishWeight system on Windows

Usage:
python build_windows.py
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("✗ PyInstaller not installed")
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install PyInstaller")
        return False

def build_exe():
    """Build executable file"""
    print("Starting build process...")
    
    # Clean previous build files
    if os.path.exists("build"):
        print("Cleaning build directory...")
        shutil.rmtree("build")
    
    if os.path.exists("dist"):
        print("Cleaning dist directory...")
        shutil.rmtree("dist")
    
    # Remove auto-generated spec file if exists
    if os.path.exists("DishWeight.spec"):
        os.remove("DishWeight.spec")
    
    # Build command with explicit parameters
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",
        "--windowed",
        "--name=DishWeight",
        "--exclude-module=PyQt5",
        "--exclude-module=PySide6",
        "--exclude-module=PyQt6",
        "--exclude-module=PySide2",
        "--exclude-module=matplotlib",
        "--exclude-module=numpy.random._pickle",
        "--exclude-module=IPython",
        "--exclude-module=jupyter",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--add-data=README.md;.",
        "--add-data=USAGE.md;.",
        "main.py"
    ]
    
    try:
        subprocess.check_call(build_cmd)
        print("✓ Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def copy_additional_files():
    """Copy additional files to output directory"""
    dist_dir = os.path.join("dist", "DishWeight")
    if not os.path.exists(dist_dir):
        print("✗ Output directory does not exist")
        return False
    
    # Copy documentation files
    files_to_copy = ["README.md", "USAGE.md"]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, dist_dir)
            print(f"✓ {file_name} copied")
    
    # Create startup instructions
    startup_info = """DishWeight - Banquet Dish Ingredient Statistics System

Usage Instructions:
1. Double-click DishWeight.exe to start the program
2. Data file dish_data.json will be automatically created in the program directory
3. The program automatically saves all data changes
4. Supports Excel format export for statistical reports

Important Notes:
- Ensure the program directory has write permissions
- Data files are automatically saved in the program directory
- For backup, manually copy the dish_data.json file
- For detailed usage instructions, refer to USAGE.md

Technical Support:
For issues, please refer to README.md or USAGE.md documentation
"""
    
    with open(os.path.join(dist_dir, "Usage Instructions.txt"), "w", encoding="utf-8") as f:
        f.write(startup_info)
    print("✓ Usage instructions created")
    
    return True

def main():
    """Main function"""
    print("=" * 60)
    print("DishWeight System - Windows EXE Build Tool")
    print("=" * 60)
    
    # Check PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("Cannot install PyInstaller, please install manually and retry")
            return False
    
    # Build executable
    if not build_exe():
        print("Build failed, please check error messages")
        return False
    
    # Copy additional files
    if not copy_additional_files():
        print("Failed to copy additional files")
        return False
    
    print("\n" + "=" * 60)
    print("Build completed successfully!")
    print("Executable location: dist/DishWeight/")
    print("Main program: dist/DishWeight/DishWeight.exe")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)