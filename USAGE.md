# DICOM Import/Export Application - Usage Guide

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/gpdahmen/DicomImporter.git
cd DicomImporter

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Application

```bash
python main.py
```

Or use the provided launcher:
```bash
python run.py
```

## Detailed Workflow

### Step 1: Launch Application
- Run `python main.py`
- The main window will appear with a modern dark theme interface

### Step 2: Select Source Directory
- Click "Browse Source" button
- Navigate to the directory containing DICOM files
  - For CD/DVD: Select the drive letter (e.g., D:\)
  - For USB: Select the USB drive or folder
  - For local folder: Select any folder with DICOM files
- The selected path will appear in the source directory field

### Step 3: Choose Destination Type

#### Option A: Export to Folder
1. Select the "Folder" radio button
2. Click "Browse Folder"
3. Select or create the destination folder
4. The application will copy all DICOM files to this location

#### Option B: Export to PACS Server
1. Select the "PACS Server" radio button
2. Configure the PACS connection:
   - **AE Title (This App)**: Your application's identification (default: DICOM_IMPORTER)
   - **Called AE Title**: The PACS server's AE title (commonly: ANY-SCP, PACS, or specific name)
   - **PACS IP Address**: IP address of the PACS server (e.g., 192.168.1.100)
   - **PACS Port**: Port number (commonly 11112 or 104)

### Step 4: Start Import/Export
1. Click "Start Import/Export" button
2. The application will:
   - Phase 1: Cache DICOM files (progress bar shows scanning/caching)
   - Phase 2: Export to destination (progress bar shows export progress)
   - Phase 3: Cleanup temporary files
3. Monitor the Activity Log for detailed progress information
4. Wait for "Operation completed successfully!" message

### Step 5: Review Results
- Check the Activity Log for summary:
  - Number of files found
  - Number of DICOM files cached
  - Number of files successfully exported
- For folder exports: Verify files in destination folder
- For PACS exports: Verify files appear in PACS system

## Understanding the Caching Process

### Why Does It Cache?

The application uses a two-phase process:
1. **Cache Phase**: Copy all DICOM files to temporary storage
2. **Export Phase**: Send from cache to final destination

**Benefits:**
- **Speed**: Sequential reading from CD/DVD is 10-100x faster than random access
- **Reliability**: Reduces disc read errors and wear
- **Progress**: Better progress tracking and error recovery
- **Network**: Faster PACS transfers from local cache vs. optical media

### Cache Location

- Temporary cache: `%TEMP%\dicom_cache_XXXXXX` (Windows) or `/tmp/dicom_cache_XXXXXX` (Linux/Mac)
- Automatically cleaned up after export
- For maximum speed, configure %TEMP% to point to a RAM disk if available

## DICOM File Validation

The application validates DICOM files by:
1. Checking for the "DICM" magic bytes at offset 128
2. This ensures only valid medical imaging files are processed
3. Non-DICOM files (text files, images, etc.) are automatically skipped

## Supported DICOM Types

The application supports common medical imaging types:
- CT (Computed Tomography)
- MR (Magnetic Resonance)
- CR (Computed Radiography)
- DX (Digital X-Ray)
- US (Ultrasound)
- XA (X-Ray Angiography)
- PT (Positron Emission Tomography)
- RT (Radiotherapy)
- SC (Secondary Capture)

## Troubleshooting

### "No DICOM files found"
- Verify the source directory contains DICOM files
- Check that files have the DICM header (not all .dcm files are valid DICOM)
- Ensure you have read permissions on the source directory

### PACS Connection Failed
- Verify IP address and port are correct
- Check network connectivity: `ping <PACS_IP>`
- Verify PACS server is running and accepting connections
- Confirm AE titles match PACS configuration
- Check firewall settings

### Application Slow on CD/DVD
- This is normal - the caching process reads all files sequentially
- Once caching completes, export is fast
- Consider using a RAM disk for %TEMP% for even faster caching

### Files Not Appearing in Destination
- Check Activity Log for errors
- Verify write permissions on destination folder
- For PACS: Check PACS server logs for import errors

## Advanced Configuration

### RAM Disk Setup (Windows)

For maximum performance with optical media:

1. Install RAM disk software (e.g., ImDisk, SoftPerfect RAM Disk)
2. Create a RAM disk (e.g., R:\) with at least 2GB
3. Set environment variable: `TEMP=R:\Temp`
4. Restart the application

The cache will now use RAM, providing:
- Near-instant read/write speeds
- No SSD wear
- Faster overall operation

### PACS Testing

To test PACS connectivity without the GUI:

```python
from dicom_engine import DicomEngine

engine = DicomEngine()
# First cache some DICOM files
engine.cache_files('/path/to/dicoms')
# Then test PACS sending
result = engine.send_to_pacs(
    ae_title='TEST_APP',
    pacs_ip='127.0.0.1',
    pacs_port=11112,
    called_ae_title='ANY-SCP'
)
print(f"Sent {result} files")
engine.cleanup()
```

## Activity Log Messages

### Normal Operation Messages
- `"Created cache directory: ..."` - Cache created successfully
- `"Found X files to check"` - Scanning complete
- `"Cached: filename (X/Y)"` - File copied to cache
- `"Caching complete: X DICOM files cached"` - Cache phase done
- `"Copied: filename (X/Y)"` - File exported to folder
- `"Sent: filename (X/Y)"` - File sent to PACS
- `"Operation completed successfully!"` - All done

### Error Messages
- `"ERROR: Please select a valid source directory"` - No source selected
- `"ERROR: Please fill in all PACS configuration fields"` - Missing PACS config
- `"Failed to establish association with PACS"` - PACS connection failed
- `"Error caching filename: ..."` - Problem reading a file
- `"PACS connection error: ..."` - Network or PACS issue

## Tips for Best Performance

1. **For CD/DVD imports**: Let the caching complete before doing anything else
2. **For network folders**: Source and destination on same network segment is fastest
3. **For PACS exports**: Local cache to PACS is very fast, typically 100+ images/second
4. **For large datasets**: Monitor disk space - ensure temp drive has enough room
5. **For multiple imports**: Clear log between operations for better readability

## Technical Architecture Summary

```
Source Media (CD/DVD/USB)
         ↓
    [Cache Phase]
         ↓
Temporary Local Storage (%TEMP%)
         ↓
    [Export Phase]
         ↓
Destination (Folder or PACS)
         ↓
    [Cleanup Phase]
         ↓
   Cache Removed
```

## Command Line Usage (Advanced)

While the application is GUI-based, you can also use the engine programmatically:

```python
from dicom_engine import DicomEngine

# Create engine with custom logging
def my_logger(msg):
    print(f"[LOG] {msg}")

engine = DicomEngine(log_callback=my_logger)

# Cache files
cached, total = engine.cache_files('/mnt/cdrom')

# Export to folder
if cached > 0:
    engine.send_to_folder('/home/user/dicom_export')
    
# Or export to PACS
# engine.send_to_pacs('MY_AE', '192.168.1.10', 11112)

# Cleanup
engine.cleanup()
```

## File Naming

- **Cached files**: `dicom_NNNNNN.dcm` (sequential numbering)
- **Exported files** (folder): `export_NNNNNN.dcm` (sequential numbering)
- **Exported files** (PACS): Original DICOM metadata preserved

## Support and Feedback

For issues or questions:
- Check the Activity Log for detailed error messages
- Review this guide for troubleshooting steps
- Visit the GitHub repository for updates and issue reporting
