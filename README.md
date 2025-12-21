# DicomImporter

A .NET console application designed to facilitate the efficient import of DICOM files from external media (such as CDs, DVDs, or USB drives) and their export to either a local network folder or a PACS (Picture Archiving and Communication System) server.

## Features

- **Import DICOM Files**: Import DICOM files from external media (CDs, DVDs, USB drives) to a staging directory
- **Export to Network Folder**: Export DICOM files to a local or network folder
- **Export to PACS Server**: Send DICOM files to a PACS server using DICOM C-STORE protocol
- **PACS Connectivity Test**: Verify connection to PACS servers using C-ECHO
- **DICOM File Information**: Display metadata from DICOM files
- **Automatic Validation**: Validates DICOM file formats during import

## Requirements

- .NET 10.0 or later
- fo-dicom library (automatically installed via NuGet)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gpdahmen/DicomImporter.git
cd DicomImporter
```

2. Build the project:
```bash
dotnet build
```

3. Run the application:
```bash
dotnet run --project src/DicomImporter -- <command> [options]
```

Or build and use the executable directly:
```bash
dotnet build -c Release
./src/DicomImporter/bin/Release/net10.0/DicomImporter <command> [options]
```

## Usage

### Import DICOM Files from External Media

Import DICOM files from a CD, DVD, or USB drive to a staging directory:

```bash
DicomImporter import <source-path> <staging-path>
```

Example:
```bash
DicomImporter import /media/cdrom /tmp/dicom-staging
```

This command:
- Recursively scans the source directory for DICOM files
- Validates each file as a valid DICOM format
- Copies valid DICOM files to the staging directory
- Generates unique filenames based on patient ID and study information

### Export DICOM Files to Network Folder

Export DICOM files from staging to a local or network folder:

```bash
DicomImporter export-folder <source-path> <destination-path>
```

Example:
```bash
DicomImporter export-folder /tmp/dicom-staging /mnt/network/dicom
```

### Export DICOM Files to PACS Server

Send DICOM files to a PACS server using the DICOM C-STORE protocol:

```bash
DicomImporter export-pacs <source-path> <pacs-host> <pacs-port> <pacs-ae-title> [client-ae-title]
```

Parameters:
- `source-path`: Directory containing DICOM files to export
- `pacs-host`: PACS server hostname or IP address
- `pacs-port`: PACS server port (typically 104)
- `pacs-ae-title`: PACS Application Entity Title
- `client-ae-title`: Optional client AE title (default: DICOM_IMPORTER)

Example:
```bash
DicomImporter export-pacs /tmp/dicom-staging 192.168.1.100 104 PACS_SERVER
```

### Test PACS Connectivity

Verify connection to a PACS server using DICOM C-ECHO:

```bash
DicomImporter test-pacs <pacs-host> <pacs-port> <pacs-ae-title> [client-ae-title]
```

Example:
```bash
DicomImporter test-pacs 192.168.1.100 104 PACS_SERVER
```

### Display DICOM File Information

View metadata from a DICOM file:

```bash
DicomImporter info <dicom-file-path>
```

Example:
```bash
DicomImporter info /tmp/dicom-staging/sample.dcm
```

This displays:
- Patient ID
- Patient Name
- Study Date
- Modality
- Study Description
- Study Instance UID

### Show Help

Display help information:

```bash
DicomImporter help
```

## Typical Workflow

1. **Import from External Media**:
   ```bash
   DicomImporter import /media/cdrom /tmp/dicom-staging
   ```

2. **Export to Network Folder**:
   ```bash
   DicomImporter export-folder /tmp/dicom-staging /mnt/network/dicom
   ```

   OR

3. **Export to PACS Server**:
   ```bash
   # First, test connectivity
   DicomImporter test-pacs 192.168.1.100 104 PACS_SERVER
   
   # Then export files
   DicomImporter export-pacs /tmp/dicom-staging 192.168.1.100 104 PACS_SERVER
   ```

## Technical Details

### DICOM Import Process

1. Recursively scans source directory for all files
2. Attempts to open each file as a DICOM file
3. Validates DICOM format using fo-dicom library
4. Extracts metadata (Patient ID, Study UID, SOP Instance UID)
5. Generates unique filename to prevent collisions
6. Copies to staging directory

### DICOM Export Process

**To Folder:**
- Copies DICOM files to specified destination
- Preserves original filenames
- Creates destination directory if needed

**To PACS:**
- Establishes DICOM connection to PACS server
- Uses DICOM C-STORE protocol to send files
- Provides per-file status feedback
- Handles connection errors gracefully

### Dependencies

- **fo-dicom** (5.2.5): Open-source DICOM implementation for .NET
  - Provides DICOM file reading/writing
  - Implements DICOM network protocols (C-STORE, C-ECHO)
  - Handles DICOM data element parsing

## Error Handling

The application includes comprehensive error handling:
- Invalid DICOM files are skipped during import
- Non-existent directories are reported
- PACS connection failures are handled gracefully
- Individual file errors don't stop batch operations

## License

This project is open source and available under standard licensing terms.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Support

For issues, questions, or contributions, please use the GitHub issue tracker.