#!/usr/bin/env python3
"""
Launch script for DICOM Import/Export Application

This script provides a simple way to start the application.
"""

import sys

try:
    import customtkinter
    import pydicom
    import pynetdicom
except ImportError as e:
    print("Error: Required dependencies not installed.")
    print(f"Missing: {e.name}")
    print("\nPlease install dependencies with:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

# Launch the application
if __name__ == "__main__":
    from main import main
    main()
