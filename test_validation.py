#!/usr/bin/env python3
"""
Test script to validate the DICOM Importer application structure
and PyInstaller build configuration
"""

import os
import sys
import subprocess


def test_files_exist():
    """Test that all required files exist"""
    print("Testing file existence...")
    required_files = [
        'main.py',
        'build.py',
        'requirements.txt',
        'README.md',
        '.gitignore'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
        else:
            print(f"  ✓ {file}")
    
    if missing:
        print(f"  ✗ Missing files: {', '.join(missing)}")
        return False
    
    print("  All required files exist ✓")
    return True


def test_requirements():
    """Test that requirements.txt contains necessary packages"""
    print("\nTesting requirements.txt...")
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    required_packages = ['pydicom', 'Pillow', 'numpy', 'pyinstaller']
    missing = []
    
    for package in required_packages:
        if package.lower() in content.lower():
            print(f"  ✓ {package}")
        else:
            missing.append(package)
    
    if missing:
        print(f"  ✗ Missing packages: {', '.join(missing)}")
        return False
    
    print("  All required packages listed ✓")
    return True


def test_main_py_structure():
    """Test that main.py has the correct structure"""
    print("\nTesting main.py structure...")
    with open('main.py', 'r') as f:
        content = f.read()
    
    checks = {
        'main() function': 'def main():',
        '__main__ entry point': 'if __name__ == "__main__":',
        'pydicom import': 'import pydicom',
        'Pillow import': 'from PIL import Image',
        'numpy import': 'import numpy',
        'tkinter import': 'import tkinter'
    }
    
    all_passed = True
    for check_name, check_string in checks.items():
        if check_string in content:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name} not found")
            all_passed = False
    
    return all_passed


def test_build_py_structure():
    """Test that build.py has the correct PyInstaller configuration"""
    print("\nTesting build.py structure...")
    with open('build.py', 'r') as f:
        content = f.read()
    
    checks = {
        '--onefile option': '--onefile',
        '--noconsole option': '--noconsole',
        'main.py entry point': 'main.py',
        'Platform awareness': 'sys.platform'
    }
    
    all_passed = True
    for check_name, check_string in checks.items():
        if check_string in content:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name} not found")
            all_passed = False
    
    return all_passed


def test_readme():
    """Test that README.md contains installation and execution instructions"""
    print("\nTesting README.md...")
    with open('README.md', 'r') as f:
        content = f.read()
    
    checks = {
        'Installation instructions': 'Installation',
        'Build instructions': 'Building the Executable',
        'Usage instructions': 'Usage',
        'PyInstaller mention': 'PyInstaller',
        'Requirements mention': 'requirements.txt',
        'Distribution instructions': 'Distribution'
    }
    
    all_passed = True
    for check_name, check_string in checks.items():
        if check_string in content:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name} not found")
            all_passed = False
    
    return all_passed


def test_gitignore():
    """Test that .gitignore excludes build artifacts"""
    print("\nTesting .gitignore...")
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    checks = {
        'build/ directory': 'build/',
        'dist/ directory': 'dist/',
        '__pycache__': '__pycache__',
        '.spec files': '*.spec'
    }
    
    all_passed = True
    for check_name, check_string in checks.items():
        if check_string in content:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name} not found")
            all_passed = False
    
    return all_passed


def test_python_syntax():
    """Test that Python files have valid syntax"""
    print("\nTesting Python syntax...")
    python_files = ['main.py', 'build.py']
    
    all_passed = True
    for file in python_files:
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', file],
            capture_output=True
        )
        if result.returncode == 0:
            print(f"  ✓ {file} syntax is valid")
        else:
            print(f"  ✗ {file} syntax error:")
            print(f"    {result.stderr.decode()}")
            all_passed = False
    
    return all_passed


def main():
    """Run all tests"""
    print("=" * 60)
    print("DICOM Importer - Validation Tests")
    print("=" * 60)
    
    tests = [
        test_files_exist,
        test_requirements,
        test_main_py_structure,
        test_build_py_structure,
        test_readme,
        test_gitignore,
        test_python_syntax
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if all(results):
        print("\n✓ All validation tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
