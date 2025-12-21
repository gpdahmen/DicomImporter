# DICOM Import/Export Application

A modern GUI application for efficient import of DICOM files from external media (CDs, DVDs, USB drives) and export to local folders or PACS servers.

## Features

- **Optimized Import**: Uses a caching mechanism to copy files to temporary local storage first, drastically reducing seek times on optical media
- **Modern GUI**: User-friendly interface built with customtkinter
- **PACS Integration**: Supports standard DICOM C-STORE operations via pynetdicom
- **Multi-threaded**: Background operations keep the UI responsive
- **Comprehensive Logging**: Real-time activity log with progress tracking

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/gpdahmen/DicomImporter.git
cd DicomImporter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Workflow

1. **Select Source Directory**: Click "Browse Source" and select the input folder/drive (e.g., D:\ for CD/DVD)

2. **Choose Destination Type**:
   - **Folder**: Select this option and browse for a target folder to copy files
   - **PACS Server**: Select this option and configure:
     - AE Title (This App): Your application's AE title (default: DICOM_IMPORTER)
     - Called AE Title: The PACS server's AE title (default: ANY-SCP)
     - PACS IP Address: IP address of the PACS server
     - PACS Port: Port number (typically 11112 or 104)

3. **Start Import/Export**: Click the "Start Import/Export" button

4. **Monitor Progress**: Watch the activity log and progress bar for real-time updates

### How It Works

The application uses a three-phase approach:

1. **Caching Phase**: Recursively scans the source directory and copies all valid DICOM files to a temporary cache. This is especially beneficial for optical media where sequential reading is much faster than random access.

2. **Export Phase**: 
   - For folder destinations: Copies files from cache to the target folder
   - For PACS destinations: Establishes a DICOM association and sends C-STORE requests for each file

3. **Cleanup Phase**: Removes the temporary cache directory

## Architecture

### DicomEngine (`dicom_engine.py`)

The core business logic module that handles:
- **`is_dicom(filepath)`**: Validates DICOM files by checking the "DICM" header signature at byte offset 128
- **`cache_files(source_dir)`**: Recursively scans and caches valid DICOM files
- **`send_to_folder(destination)`**: Copies cached files to a destination folder
- **`send_to_pacs(ae_title, ip, port)`**: Sends cached files to a PACS server via DICOM C-STORE
- **`cleanup()`**: Removes temporary cache files

### DicomApp (`main.py`)

The GUI application that:
- Provides an intuitive customtkinter-based interface
- Runs file operations in background threads to maintain UI responsiveness
- Displays real-time progress updates and logging
- Handles user input validation and error reporting

## Dependencies

- **customtkinter**: Modern GUI framework (≥5.2.0)
- **pydicom**: DICOM file parsing (≥2.4.0)
- **pynetdicom**: DICOM networking and PACS communication (≥2.0.0)

## Supported DICOM Storage Classes

The application supports the following SOP classes:
- CT Image Storage
- MR Image Storage
- Secondary Capture Image Storage
- Digital X-Ray Image Storage for Presentation
- Computed Radiography Image Storage
- Ultrasound Image Storage
- Ultrasound Multi-frame Image Storage
- X-Ray Angiographic Image Storage
- Positron Emission Tomography Image Storage
- RT Image Storage

## Technical Notes

### Why Caching?

Optical drives (CD/DVD) have poor random access performance. Reading files sequentially and caching them locally before export provides:
- Significantly faster overall operation time
- Reduced wear on optical drives
- More reliable file transfers
- Better progress tracking

### RAM Disk Optimization

For maximum performance, you can configure your system to use a RAM disk for the temporary directory (%TEMP%). The application will automatically use it if available.

## OS Support

The application is designed primarily for Windows but is cross-platform compatible and should work on Linux and macOS as well.

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/gpdahmen/DicomImporter).