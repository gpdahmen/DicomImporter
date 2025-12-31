#!/usr/bin/env python3
"""
Build script for creating standalone executable of DICOM Importer
Uses PyInstaller to create a single executable file
"""

import subprocess
import sys
import os
import shutil


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} is installed")
        return True
    except ImportError:
        print("✗ PyInstaller is not installed")
        print("  Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True


def clean_build_directories():
    """Clean up previous build artifacts"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}/...")
            shutil.rmtree(dir_name)
    
    # Remove spec file if exists
    if os.path.exists('main.spec'):
        os.remove('main.spec')
        print("Removed main.spec")


def build_executable():
    """Build the executable using PyInstaller"""
    print("\n" + "=" * 60)
    print("Building DICOM Importer executable...")
    print("=" * 60 + "\n")
    
    # PyInstaller command with options
    command = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",           # Create a single executable file
        "--noconsole",         # Don't show console window (GUI app)
        "--name=DicomImporter", # Name of the executable
        "--icon=NONE",         # No icon (can be added later)
        "main.py"              # Entry point
    ]
    
    print(f"Running: {' '.join(command)}\n")
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error code {e.returncode}")
        return False


def verify_build():
    """Verify that the executable was created"""
    exe_path = os.path.join('dist', 'DicomImporter.exe')
    if os.path.exists(exe_path):
        file_size = os.path.getsize(exe_path) / (1024 * 1024)  # Convert to MB
        print(f"\n✓ Build successful!")
        print(f"  Executable: {exe_path}")
        print(f"  Size: {file_size:.2f} MB")
        return True
    else:
        print(f"\n✗ Build failed - executable not found at {exe_path}")
        return False


def main():
    """Main build process"""
    print("DICOM Importer - Build Script")
    print("=" * 60)
    
    # Check if we're in the correct directory
    if not os.path.exists('main.py'):
        print("✗ Error: main.py not found in current directory")
        print("  Please run this script from the project root directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_pyinstaller():
        print("✗ Failed to install PyInstaller")
        sys.exit(1)
    
    # Clean previous builds
    print("\nCleaning previous build artifacts...")
    clean_build_directories()
    
    # Build executable
    if not build_executable():
        sys.exit(1)
    
    # Verify build
    if not verify_build():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Build process completed successfully!")
    print("=" * 60)
    print("\nThe executable is located in the 'dist' directory.")
    print("You can now distribute DicomImporter.exe to other Windows PCs.")
    print("\nNote: The executable includes all dependencies and does not")
    print("      require Python or any other installations on the target PC.")


if __name__ == "__main__":
    main()
