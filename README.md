# DICOM Importer

A lightweight Python GUI application for importing and viewing DICOM medical imaging files.

## Features

- Import individual DICOM files
- Import entire folders containing DICOM files (with recursive scanning)
- Display file information (name, path, size)
- Simple and intuitive graphical user interface
- Cross-platform support (Windows, macOS, Linux)

## Installation

### Prerequisites

- Python 3.7 or higher
- tkinter (usually included with Python)

### Installing Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running from Source

```bash
python main.py
```

### Building Standalone Executable

To build a standalone `.exe` file (Windows) or executable (Linux/macOS):

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Build the executable
pyinstaller --onefile --windowed --name DicomImporter main.py
```

The executable will be created in the `dist/` directory.

#### Build Options Explained

- `--onefile`: Creates a single executable file
- `--windowed`: Hides the console window (GUI only)
- `--name DicomImporter`: Names the output executable

## CI/CD Pipeline

This repository includes a GitHub Actions workflow that automatically builds a Windows `.exe` file.

### Workflow Triggers

- Push to `main` branch
- Pull request creation

### Artifacts

After a successful build, the `.exe` file is available as a downloadable artifact:

1. Go to the [Actions](../../actions) tab
2. Click on the latest workflow run
3. Download the artifact under "Artifacts"
4. Extract the ZIP file to get `DicomImporter.exe`

Artifacts are retained for 90 days.

## Development

### Project Structure

```
DicomImporter/
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

### Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
4. Make your changes
5. Test locally before committing

### Testing the Build

Before committing changes, test that the application builds successfully:

```bash
# Test the build process
pyinstaller --onefile --windowed --name DicomImporter main.py

# Check that the executable was created
ls -lh dist/DicomImporter*
```

## Troubleshooting

### PyInstaller Build Issues

If you encounter issues building with PyInstaller:

1. **Missing tkinter**: Ensure tkinter is installed with your Python distribution
   - Windows: tkinter is included by default
   - Linux: `sudo apt-get install python3-tk`
   - macOS: tkinter is included by default

2. **Import errors**: Make sure all dependencies are in `requirements.txt`

3. **Large executable size**: This is normal for PyInstaller bundles as they include Python runtime

### Application Issues

- **DICOM files not recognized**: Ensure files have `.dcm`, `.dicom`, or `.dic` extensions, or no extension
- **Folder import not working**: Check that you have read permissions for the folder

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.