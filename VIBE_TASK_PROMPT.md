# ViBE Task Prompt: DICOM Import/Export Application

## Task Overview

Develop a comprehensive Python command-line application for importing, exporting, and managing DICOM (Digital Imaging and Communications in Medicine) medical image files. The application must provide robust functionality for healthcare professionals, researchers, and developers working with medical imaging data.

## Core Objectives

### 1. DICOM File Operations
- **Import Capability**: Read DICOM files from the filesystem with full metadata extraction
- **Export Capability**: Write DICOM files to specified locations while maintaining data integrity
- **File Validation**: Ensure DICOM files conform to the standard before processing
- **Error Handling**: Provide clear error messages for invalid or corrupted files

### 2. Metadata Management
- **Extraction**: Automatically extract key DICOM tags including patient information, study details, and imaging parameters
- **Display**: Present metadata in a human-readable format with proper formatting
- **Completeness**: Handle missing or optional DICOM tags gracefully
- **Standard Compliance**: Support common DICOM tags defined in the DICOM standard

### 3. Pixel Data Processing
- **Data Access**: Extract pixel arrays from DICOM files as numpy arrays
- **Format Support**: Handle various pixel data encodings (grayscale, color, multi-frame)
- **Statistics**: Calculate and display pixel data statistics (min, max, mean, shape)
- **Type Conversion**: Properly handle different pixel data types (uint8, uint16, int16, etc.)

### 4. File Creation
- **Array to DICOM**: Create valid DICOM files from numpy pixel arrays
- **Metadata Assignment**: Allow custom metadata to be set on newly created files
- **Standard Compliance**: Ensure created files conform to DICOM standards
- **Flexibility**: Support various modalities and image types

### 5. User Interface
- **Command-Line Interface**: Intuitive CLI with clear command structure
- **Help System**: Comprehensive help messages and usage examples
- **Output Formatting**: Well-formatted, readable output for all operations
- **Progress Indication**: Clear success/failure messages for operations

## Scope Definition

### In Scope

#### Functional Requirements
1. **DICOM File Import**
   - Read DICOM files using pydicom library
   - Extract and organize metadata
   - Load pixel data into memory
   - Validate file format

2. **DICOM File Export**
   - Write DICOM files to disk
   - Preserve all metadata and pixel data
   - Create output directories as needed
   - Ensure DICOM compliance

3. **Information Display**
   - Show patient demographics
   - Display study and series information
   - Present imaging parameters
   - Show pixel data properties
   - List all available DICOM tags

4. **File Creation**
   - Generate DICOM from numpy arrays
   - Set mandatory DICOM tags
   - Support custom metadata
   - Handle various image dimensions

5. **Command-Line Interface**
   - Three main commands: import, export, info
   - Argument parsing and validation
   - Help and usage information
   - Error reporting

#### Technical Requirements
1. **Language**: Python 3.7+
2. **Core Libraries**:
   - pydicom: DICOM file operations
   - numpy: Pixel data manipulation
   - pathlib: File path handling
   - argparse: Command-line parsing

3. **Code Quality**:
   - Comprehensive docstrings for all modules, classes, and functions
   - Type hints for function parameters and return values
   - Inline comments explaining complex logic
   - Professional coding standards

4. **Testing**:
   - Unit tests for all major functionality
   - Test coverage for import/export operations
   - Test coverage for metadata extraction
   - Test coverage for pixel data handling
   - Error condition testing

5. **Documentation**:
   - Comprehensive README.md
   - Module-level documentation
   - Function and class documentation
   - Usage examples and code samples
   - Installation instructions

### Out of Scope

#### Features NOT Included
1. **Advanced DICOM Features**:
   - DICOM network operations (C-STORE, C-FIND, C-MOVE)
   - PACS integration
   - DICOM query/retrieve
   - DICOM worklist management

2. **Image Processing**:
   - Image filtering or enhancement
   - Format conversion (JPEG, PNG, etc.)
   - Image registration or fusion
   - 3D visualization or rendering

3. **Database Operations**:
   - DICOM database creation
   - SQL integration
   - Full-text search
   - Indexing services

4. **GUI**:
   - Graphical user interface
   - Web interface
   - Interactive visualization
   - Drag-and-drop functionality

5. **Advanced Analysis**:
   - Machine learning integration
   - Automated diagnosis
   - Image segmentation
   - Quantitative analysis

6. **Multi-User Features**:
   - User authentication
   - Role-based access control
   - Audit logging
   - Multi-tenant support

## Deliverables

### 1. Source Code Files

#### dicom_engine.py
- **Purpose**: Core DICOM processing engine
- **Requirements**:
  - DicomEngine class with all methods
  - Comprehensive docstrings for class and methods
  - Type hints for all function parameters
  - Inline comments for complex logic
  - Error handling with appropriate exceptions

#### main.py
- **Purpose**: Command-line interface
- **Requirements**:
  - Argument parser setup
  - Command handlers (import, export, info)
  - Output formatting functions
  - Comprehensive docstrings
  - Error handling and user feedback

#### test_dicom.py
- **Purpose**: Unit test suite
- **Requirements**:
  - TestDicomEngine class with all test methods
  - Test coverage for all major functionality
  - Docstrings explaining each test's purpose
  - Sample data creation helpers
  - Temporary file management

### 2. Documentation

#### README.md
- **Contents**:
  - High-level program description
  - Purpose and use cases
  - Main features overview
  - Installation instructions
  - Usage examples for all commands
  - Architecture description
  - Testing instructions
  - Technical requirements
  - Project structure
  - Contributing guidelines

#### Code Documentation
- **Requirements**:
  - Every function has a docstring with:
    - Purpose description
    - Parameter documentation
    - Return value documentation
    - Usage examples (where appropriate)
    - Exception documentation
  - Every class has a docstring with:
    - Purpose description
    - Attribute documentation
    - Usage examples
  - Inline comments for:
    - Complex algorithms
    - Non-obvious logic
    - Important implementation decisions

### 3. Testing Artifacts
- Unit test suite (test_dicom.py)
- Test execution results
- Test coverage report (if applicable)

## Implementation Guidelines

### Code Style
1. **PEP 8 Compliance**: Follow Python's style guide
2. **Naming Conventions**:
   - Classes: PascalCase (e.g., DicomEngine)
   - Functions: snake_case (e.g., import_dicom)
   - Constants: UPPER_SNAKE_CASE (e.g., MAX_FILE_SIZE)
   - Private methods: _leading_underscore (e.g., _extract_metadata)

3. **Documentation Format**:
   - Use Google-style or NumPy-style docstrings consistently
   - Include type information in docstrings
   - Provide examples in docstrings where helpful

4. **Error Handling**:
   - Use specific exception types
   - Provide informative error messages
   - Log errors appropriately
   - Don't suppress exceptions silently

### Testing Strategy
1. **Unit Tests**: Test individual functions in isolation
2. **Integration Tests**: Test command flow from CLI to engine
3. **Edge Cases**: Test boundary conditions and error cases
4. **Mock Data**: Use temporary files and synthetic DICOM data
5. **Cleanup**: Ensure tests clean up temporary files

### Documentation Standards
1. **Completeness**: Document all public APIs
2. **Clarity**: Use clear, professional language
3. **Examples**: Include usage examples
4. **Maintenance**: Keep documentation in sync with code
5. **Audience**: Target developers who will maintain the code

## Success Criteria

### Functional Success
- ✅ Application can import valid DICOM files
- ✅ Application can export DICOM files
- ✅ Metadata is extracted and displayed correctly
- ✅ Pixel data can be accessed and analyzed
- ✅ New DICOM files can be created from arrays
- ✅ All commands work as documented

### Quality Success
- ✅ All functions have comprehensive docstrings
- ✅ Code includes appropriate inline comments
- ✅ Type hints are used throughout
- ✅ Error handling is robust and user-friendly
- ✅ Unit tests cover all major functionality
- ✅ All tests pass successfully

### Documentation Success
- ✅ README.md provides comprehensive overview
- ✅ Installation instructions are clear and complete
- ✅ Usage examples are provided for all commands
- ✅ Code documentation is professional and consistent
- ✅ Architecture is clearly explained

## Timeline and Milestones

### Phase 1: Core Engine Development
- Implement DicomEngine class
- Add import/export functionality
- Implement metadata extraction
- Add comprehensive docstrings

### Phase 2: Command-Line Interface
- Implement argument parsing
- Create command handlers
- Add output formatting
- Include help system

### Phase 3: Testing
- Write unit tests
- Test all major features
- Test error conditions
- Verify test coverage

### Phase 4: Documentation
- Write comprehensive README.md
- Review and enhance code documentation
- Verify all docstrings are complete
- Add usage examples

### Phase 5: Quality Assurance
- Review code for quality
- Verify documentation completeness
- Run full test suite
- Final validation

## Risk Considerations

### Technical Risks
1. **DICOM Complexity**: DICOM standard is complex with many optional features
   - Mitigation: Focus on common use cases and essential features

2. **File Format Variations**: DICOM files can vary significantly
   - Mitigation: Use pydicom library which handles most variations

3. **Large Files**: Medical images can be very large
   - Mitigation: Stream data where possible, document limitations

### Quality Risks
1. **Incomplete Documentation**: Risk of missing important details
   - Mitigation: Review checklist, peer review

2. **Test Coverage Gaps**: Risk of untested code paths
   - Mitigation: Systematic test planning, code review

## Acceptance Criteria

The task is complete when:
1. All source code files (dicom_engine.py, main.py, test_dicom.py) are created
2. Every function in the codebase has a detailed docstring
3. Key sections have inline comments explaining logic
4. README.md contains comprehensive documentation
5. All unit tests pass successfully
6. Code follows professional standards and is consistent
7. Application can successfully import, export, and display DICOM files
8. This ViBE task prompt document is included in the repository

## References

### Standards and Specifications
- DICOM Standard: https://www.dicomstandard.org/
- Python PEP 8: https://www.python.org/dev/peps/pep-0008/
- Python PEP 257 (Docstrings): https://www.python.org/dev/peps/pep-0257/

### Libraries and Tools
- pydicom: https://pydicom.github.io/
- numpy: https://numpy.org/
- Python unittest: https://docs.python.org/3/library/unittest.html

### Medical Imaging Resources
- DICOM Standard Browser: https://dicom.innolitics.com/
- Medical Image Analysis: Various academic and professional resources

## Notes

This application is designed as a starting point for DICOM file management. It provides essential functionality while maintaining clean, well-documented code that can be extended for more advanced features in the future. The focus is on reliability, usability, and maintainability.