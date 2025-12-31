"""
DICOM Import/Export Application - Main Module

This is the main entry point for the DICOM Import/Export command-line application.
It provides a user-friendly interface for importing DICOM medical image files,
viewing their metadata, and exporting them to different locations.

The application supports:
    - Importing DICOM files from the filesystem
    - Viewing patient and study metadata
    - Extracting and displaying pixel data information
    - Exporting DICOM files to new locations
    - Creating new DICOM files from pixel arrays

Usage:
    python main.py import <file_path>
    python main.py export <input_path> <output_path>
    python main.py info <file_path>

Author: DICOM Import/Export Team
Version: 1.0.0
"""

import sys
import argparse
from pathlib import Path
from typing import Optional, List
from dicom_engine import DicomEngine


def setup_argument_parser() -> argparse.ArgumentParser:
    """
    Set up and configure the command-line argument parser.
    
    Creates an ArgumentParser with all supported commands and their respective
    arguments. This provides a structured way for users to interact with the
    DICOM import/export functionality via command line.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser with all commands defined
    
    Commands:
        import: Import and display metadata from a DICOM file
        export: Export a DICOM file to a new location
        info: Display detailed information about a DICOM file
        
    Example:
        >>> parser = setup_argument_parser()
        >>> args = parser.parse_args(['import', 'scan.dcm'])
    """
    # Create the main parser with a description of the application
    parser = argparse.ArgumentParser(
        description='DICOM Import/Export Application - Manage medical imaging files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s import /path/to/dicom/file.dcm
      Import and display metadata from a DICOM file
      
  %(prog)s export input.dcm output.dcm
      Export a DICOM file to a new location
      
  %(prog)s info scan.dcm
      Display detailed information about a DICOM file
        """
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Command: import - Import a DICOM file and display its metadata
    import_parser = subparsers.add_parser(
        'import',
        help='Import a DICOM file and display its metadata'
    )
    import_parser.add_argument(
        'file_path',
        type=str,
        help='Path to the DICOM file to import'
    )
    
    # Command: export - Export a DICOM file to a new location
    export_parser = subparsers.add_parser(
        'export',
        help='Export a DICOM file to a new location'
    )
    export_parser.add_argument(
        'input_path',
        type=str,
        help='Path to the input DICOM file'
    )
    export_parser.add_argument(
        'output_path',
        type=str,
        help='Path where the DICOM file will be exported'
    )
    
    # Command: info - Display detailed information about a DICOM file
    info_parser = subparsers.add_parser(
        'info',
        help='Display detailed information about a DICOM file'
    )
    info_parser.add_argument(
        'file_path',
        type=str,
        help='Path to the DICOM file to analyze'
    )
    
    return parser


def import_dicom_file(file_path: str) -> Optional[DicomEngine]:
    """
    Import a DICOM file and display its metadata.
    
    Creates a DicomEngine instance, loads the specified DICOM file, and prints
    its metadata to the console in a formatted, human-readable way.
    
    Args:
        file_path (str): Path to the DICOM file to import
    
    Returns:
        Optional[DicomEngine]: DicomEngine instance with loaded file if successful,
                              None if import failed
    
    Example:
        >>> engine = import_dicom_file("scan.dcm")
        >>> if engine:
        ...     print("Import successful")
    """
    # Create a new DicomEngine instance
    engine = DicomEngine()
    
    print(f"\n{'='*60}")
    print(f"Importing DICOM file: {file_path}")
    print(f"{'='*60}\n")
    
    try:
        # Attempt to import the DICOM file
        success = engine.import_dicom(file_path)
        
        if not success:
            print("❌ Failed to import DICOM file")
            return None
        
        # Import successful - display metadata
        print("✓ DICOM file imported successfully\n")
        
        # Get and display metadata
        metadata = engine.get_metadata()
        print("DICOM Metadata:")
        print("-" * 60)
        
        # Display each metadata field in a formatted way
        for key, value in metadata.items():
            # Format the key for better readability (convert camelCase to spaced)
            formatted_key = ''.join([' ' + c if c.isupper() else c for c in key]).strip()
            print(f"  {formatted_key:20s}: {value}")
        
        # Get pixel data information if available
        pixel_data = engine.get_pixel_data()
        if pixel_data is not None:
            print("\nPixel Data Information:")
            print("-" * 60)
            print(f"  Shape                : {pixel_data.shape}")
            print(f"  Data Type            : {pixel_data.dtype}")
            print(f"  Min Value            : {pixel_data.min()}")
            print(f"  Max Value            : {pixel_data.max()}")
        
        print(f"\n{'='*60}\n")
        
        return engine
    
    except FileNotFoundError as e:
        print(f"❌ Error: {str(e)}")
        return None
    
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None


def export_dicom_file(input_path: str, output_path: str) -> bool:
    """
    Export a DICOM file from input path to output path.
    
    Reads a DICOM file from the input location and writes it to the output location.
    This can be used to copy DICOM files while ensuring format validity, or to
    relocate files to different directories.
    
    Args:
        input_path (str): Path to the input DICOM file
        output_path (str): Path where the file will be exported
    
    Returns:
        bool: True if export was successful, False otherwise
    
    Example:
        >>> success = export_dicom_file("input.dcm", "output/copy.dcm")
        >>> if success:
        ...     print("Export completed")
    """
    print(f"\n{'='*60}")
    print(f"Exporting DICOM file")
    print(f"{'='*60}")
    print(f"  Input  : {input_path}")
    print(f"  Output : {output_path}\n")
    
    try:
        # Create engine and import the input file
        engine = DicomEngine()
        success = engine.import_dicom(input_path)
        
        if not success:
            print("❌ Failed to read input DICOM file")
            return False
        
        # Export to the output path
        success = engine.export_dicom(output_path)
        
        if success:
            print("✓ DICOM file exported successfully")
            print(f"  File saved to: {output_path}")
            print(f"\n{'='*60}\n")
            return True
        else:
            print("❌ Failed to export DICOM file")
            return False
    
    except Exception as e:
        print(f"❌ Error during export: {str(e)}")
        return False


def display_dicom_info(file_path: str) -> bool:
    """
    Display comprehensive information about a DICOM file.
    
    Reads a DICOM file and displays detailed information including all metadata,
    pixel data properties, and all available DICOM tags. This is more detailed
    than the simple import command.
    
    Args:
        file_path (str): Path to the DICOM file to analyze
    
    Returns:
        bool: True if information was successfully retrieved and displayed,
              False otherwise
    
    Example:
        >>> success = display_dicom_info("scan.dcm")
        >>> if success:
        ...     print("Information displayed successfully")
    """
    print(f"\n{'='*60}")
    print(f"DICOM File Information")
    print(f"{'='*60}")
    print(f"File: {file_path}\n")
    
    try:
        # Create engine and load the file
        engine = DicomEngine()
        success = engine.import_dicom(file_path)
        
        if not success:
            print("❌ Failed to read DICOM file")
            return False
        
        # Display file size information
        file_size = Path(file_path).stat().st_size
        print(f"File Size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")
        print()
        
        # Display metadata
        metadata = engine.get_metadata()
        print("Basic Metadata:")
        print("-" * 60)
        for key, value in metadata.items():
            formatted_key = ''.join([' ' + c if c.isupper() else c for c in key]).strip()
            print(f"  {formatted_key:20s}: {value}")
        
        # Display pixel data information
        pixel_data = engine.get_pixel_data()
        if pixel_data is not None:
            print("\nPixel Data:")
            print("-" * 60)
            print(f"  Shape                : {pixel_data.shape}")
            print(f"  Data Type            : {pixel_data.dtype}")
            print(f"  Min Value            : {pixel_data.min()}")
            print(f"  Max Value            : {pixel_data.max()}")
            print(f"  Mean Value           : {pixel_data.mean():.2f}")
            print(f"  Total Pixels         : {pixel_data.size:,}")
        
        # Display all available tags
        all_tags = engine.list_all_tags()
        if all_tags:
            print(f"\nAll DICOM Tags ({len(all_tags)} total):")
            print("-" * 60)
            # Display tags in columns for better readability
            for i in range(0, len(all_tags), 3):
                tags_line = all_tags[i:i+3]
                print("  " + "  |  ".join(f"{tag:25s}" for tag in tags_line))
        
        print(f"\n{'='*60}\n")
        return True
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main() -> int:
    """
    Main entry point for the DICOM Import/Export application.
    
    Parses command-line arguments and executes the appropriate command. Handles
    errors gracefully and provides appropriate exit codes.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    
    Exit Codes:
        0: Operation completed successfully
        1: Error occurred during operation
        2: Invalid command or arguments
    
    Example:
        >>> # Run from command line
        >>> # python main.py import scan.dcm
        >>> sys.exit(main())
    """
    # Set up argument parser
    parser = setup_argument_parser()
    
    # Parse command-line arguments
    # If no arguments provided, display help
    if len(sys.argv) == 1:
        parser.print_help()
        return 2
    
    args = parser.parse_args()
    
    # Handle different commands
    try:
        if args.command == 'import':
            # Import and display DICOM file metadata
            result = import_dicom_file(args.file_path)
            return 0 if result is not None else 1
        
        elif args.command == 'export':
            # Export DICOM file to new location
            success = export_dicom_file(args.input_path, args.output_path)
            return 0 if success else 1
        
        elif args.command == 'info':
            # Display detailed DICOM file information
            success = display_dicom_info(args.file_path)
            return 0 if success else 1
        
        else:
            # Unknown command
            print(f"Error: Unknown command '{args.command}'")
            parser.print_help()
            return 2
    
    except KeyboardInterrupt:
        # User interrupted the operation (Ctrl+C)
        print("\n\nOperation cancelled by user")
        return 1
    
    except Exception as e:
        # Unexpected error occurred
        print(f"\n❌ Unexpected error: {str(e)}")
        return 1


# Entry point when script is run directly
if __name__ == '__main__':
    # Execute main function and exit with its return code
    sys.exit(main())
