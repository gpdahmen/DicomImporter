# DICOM Import/Export Application

A comprehensive Python application for importing, exporting, and managing DICOM (Digital Imaging and Communications in Medicine) medical image files. This tool provides an easy-to-use command-line interface for working with DICOM files commonly used in medical imaging.

## Overview

DICOM is the international standard for medical images and related information. This application enables healthcare professionals, researchers, and developers to:

- **Import DICOM files** and extract metadata (patient information, study details, imaging parameters)
- **Export DICOM files** to different locations while maintaining data integrity
- **View detailed information** about DICOM files including pixel data properties
- **Create DICOM files** from numpy arrays for research and testing purposes
- **Validate DICOM files** by reading and re-exporting them

## Purpose and Use Cases

### Medical Imaging Workflows
- **Archive Management**: Import and organize DICOM files from medical imaging equipment
- **Data Migration**: Export DICOM files to new storage systems or cloud platforms
- **Quality Assurance**: Verify DICOM file integrity and metadata completeness

### Research and Development
- **Data Analysis**: Extract metadata and pixel data for statistical analysis
- **Algorithm Development**: Create test DICOM datasets for machine learning models
- **Format Conversion**: Generate DICOM files from processed image data

### Healthcare IT
- **System Integration**: Interface with PACS (Picture Archiving and Communication Systems)
- **Data Validation**: Verify DICOM compliance before importing to clinical systems
- **Metadata Extraction**: Generate reports from DICOM metadata

## Main Features

### 1. DICOM File Import
- Read DICOM files from any location on the filesystem
- Automatically extract and display key metadata
- Handle various DICOM transfer syntaxes and encodings
- Validate file integrity during import

### 2. Metadata Extraction
- Patient demographics (name, ID)
- Study information (date, description)
- Imaging parameters (modality, series description)
- Image properties (dimensions, pixel spacing)

### 3. Pixel Data Access
- Extract raw pixel arrays as numpy arrays
- Support for grayscale and color images
- Handle multi-frame (3D) DICOM files
- Calculate pixel statistics (min, max, mean)

### 4. DICOM File Export
- Write DICOM files to specified output paths
- Maintain DICOM standard compliance
- Preserve all metadata and pixel data
- Create directory structures automatically

### 5. DICOM Creation
- Generate DICOM files from numpy arrays
- Set custom metadata for new files
- Support for various image types and modalities
- Useful for testing and synthetic data generation

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Required Dependencies
```bash
pip install pydicom numpy
```

### Optional Dependencies
For image visualization and additional features:
```bash
pip install pillow matplotlib
```

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/gpdahmen/DicomImporter.git
   cd DicomImporter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Verify installation:
   ```bash
   python main.py --help
   ```

## Usage

The application provides three main commands: `import`, `export`, and `info`.

### Basic Command Structure
```bash
python main.py <command> [arguments]
```

### Command: Import
Import a DICOM file and display its metadata:

```bash
python main.py import /path/to/dicom/file.dcm
```

**Example output:**
```
============================================================
Importing DICOM file: scan.dcm
============================================================

✓ DICOM file imported successfully

DICOM Metadata:
------------------------------------------------------------
  Patient Name         : Doe^John
  Patient ID           : 12345678
  Study Date           : 20250101
  Study Description    : Brain MRI
  Modality             : MR
  Series Description   : T1 Axial
  Rows                 : 512
  Columns              : 512

Pixel Data Information:
------------------------------------------------------------
  Shape                : (512, 512)
  Data Type            : uint16
  Min Value            : 0
  Max Value            : 4095
============================================================
```

### Command: Export
Export a DICOM file to a new location:

```bash
python main.py export input.dcm output/path/output.dcm
```

**Features:**
- Creates output directories automatically if they don't exist
- Maintains full DICOM compliance in output file
- Preserves all metadata and pixel data

### Command: Info
Display comprehensive information about a DICOM file:

```bash
python main.py info /path/to/file.dcm
```

**Shows:**
- File size information
- Complete metadata listing
- Detailed pixel data statistics
- All available DICOM tags in the file

## Architecture

The application is organized into three main modules:

### 1. `dicom_engine.py` - Core Engine
The `DicomEngine` class provides the core functionality:
- **File Operations**: Reading and writing DICOM files
- **Metadata Management**: Extracting and organizing DICOM tags
- **Pixel Data Handling**: Converting between DICOM and numpy formats
- **File Creation**: Generating new DICOM files from arrays

**Key Methods:**
- `import_dicom(file_path)`: Load a DICOM file
- `export_dicom(output_path)`: Save a DICOM file
- `get_metadata()`: Retrieve metadata dictionary
- `get_pixel_data()`: Extract pixel array
- `create_dicom_from_array(array, metadata)`: Create new DICOM file

### 2. `main.py` - Command-Line Interface
Provides the user interface for the application:
- **Argument Parsing**: Handle command-line arguments
- **Command Dispatch**: Route commands to appropriate functions
- **Output Formatting**: Display results in user-friendly format
- **Error Handling**: Provide clear error messages

### 3. `test_dicom.py` - Test Suite
Comprehensive unit tests for all functionality:
- **Import Tests**: Verify file reading and metadata extraction
- **Export Tests**: Validate file writing and data preservation
- **Creation Tests**: Test DICOM generation from arrays
- **Error Handling Tests**: Ensure proper error handling

## Code Documentation

All code in this application follows professional documentation standards:

- **Module Docstrings**: Every file has a comprehensive module-level docstring explaining its purpose
- **Class Docstrings**: All classes include detailed documentation of their purpose and attributes
- **Function Docstrings**: Every function includes:
  - Purpose description
  - Parameter documentation with types
  - Return value documentation
  - Usage examples where applicable
  - Exception documentation
- **Inline Comments**: Complex logic includes explanatory comments
- **Type Hints**: Functions use type annotations for clarity

## Testing

Run the complete test suite:
```bash
python test_dicom.py
```

Run with unittest directly:
```bash
python -m unittest test_dicom.py
```

Run specific test:
```bash
python -m unittest test_dicom.TestDicomEngine.test_import_valid_dicom
```

**Test Coverage:**
- File import and validation
- Metadata extraction accuracy
- Pixel data handling
- File export functionality
- DICOM creation from arrays
- Error handling and edge cases

## Technical Requirements

### Python Version
- Python 3.7+

### Core Dependencies
- **pydicom** (≥2.0.0): DICOM file reading and writing
- **numpy** (≥1.18.0): Pixel data manipulation

### Platform Support
- Linux (tested)
- macOS (tested)
- Windows (tested)

## Project Structure
```
DicomImporter/
├── README.md              # This file - comprehensive documentation
├── main.py               # Command-line interface
├── dicom_engine.py       # Core DICOM processing engine
├── test_dicom.py         # Unit tests
├── requirements.txt      # Python dependencies
└── examples/             # Example DICOM files (if available)
```

## Contributing

Contributions are welcome! When contributing:

1. **Follow Documentation Standards**: Add comprehensive docstrings and comments
2. **Maintain Code Quality**: Ensure all tests pass
3. **Add Tests**: Include unit tests for new features
4. **Update Documentation**: Keep README.md current

## Error Handling

The application includes robust error handling:

- **File Not Found**: Clear message when input files don't exist
- **Invalid DICOM**: Graceful handling of corrupted or non-DICOM files
- **Permission Errors**: Informative messages for filesystem permission issues
- **Missing Dependencies**: Helpful installation instructions
- **Invalid Arguments**: Usage help for incorrect command-line arguments

## Best Practices

### For Users
- Always verify DICOM file paths before running commands
- Use absolute paths when possible to avoid ambiguity
- Check output directory permissions before exporting
- Validate exported files with the `info` command

### For Developers
- Read the comprehensive docstrings in each module
- Review test cases to understand expected behavior
- Follow the existing code style and documentation patterns
- Test changes with both valid and invalid inputs

## Security Considerations

When working with medical data:
- **Patient Privacy**: Remove or anonymize patient information when sharing
- **Data Integrity**: Verify DICOM files haven't been modified unexpectedly
- **Access Control**: Ensure proper file system permissions
- **Compliance**: Follow HIPAA, GDPR, or relevant regulations in your jurisdiction

## License

[Specify your license here]

## Support and Contact

For issues, questions, or contributions:
- GitHub Issues: https://github.com/gpdahmen/DicomImporter/issues
- Repository: https://github.com/gpdahmen/DicomImporter

## Version History

- **1.0.0** (2025): Initial release with comprehensive documentation
  - DICOM import/export functionality
  - Metadata extraction and display
  - Pixel data handling
  - Complete test suite
  - Comprehensive code documentation

## Acknowledgments

This application uses the pydicom library, an excellent open-source Python package for working with DICOM files. Thanks to the pydicom development team and contributors.