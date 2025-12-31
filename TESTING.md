# Testing the DICOM Importer Application

## Getting Test DICOM Files

To test the DICOM Importer application, you'll need DICOM files. Here are some options:

### Option 1: Free Sample DICOM Files

You can download free sample DICOM files from these sources:

1. **Medical Connections**: https://www.rubomedical.com/dicom_files/
   - Offers various sample DICOM files for testing

2. **OsiriX Sample Data**: https://www.osirix-viewer.com/resources/dicom-image-library/
   - Provides sample datasets

3. **DICOM Library**: https://www.dicomlibrary.com/
   - Collection of anonymized DICOM studies

### Option 2: Create Your Own Test Files

If you work in medical imaging or research, you may have access to DICOM files through your institution (ensure they're properly anonymized for testing).

## Quick Test

1. Download a sample DICOM file (usually with `.dcm` extension)
2. Run the application:
   - From source: `python main.py`
   - From executable: Double-click `DicomImporter.exe`
3. Click "Open DICOM File" and select your downloaded file
4. Verify that:
   - The image displays in the "Image Viewer" tab
   - The metadata appears in the "Metadata" tab
   - The status bar shows the loaded filename

## What to Expect

- **Image Viewer Tab**: Should display the medical image with automatic scaling
- **Metadata Tab**: Should show all DICOM tags including:
  - Patient information (usually anonymized in samples)
  - Study and series information
  - Image acquisition parameters
  - Technical metadata

## Troubleshooting Test Files

If you encounter issues loading a DICOM file:

1. **Check file format**: Ensure it's a valid DICOM file (usually `.dcm` extension)
2. **Verify file integrity**: Make sure the file isn't corrupted
3. **Check file size**: Very large files may take longer to load
4. **Look for pixel data**: Some DICOM files contain only metadata without images

## Notes on Privacy

- Always use anonymized or sample DICOM files for testing
- Never use real patient data without proper authorization and anonymization
- Sample files from the sources above are pre-anonymized for public use
