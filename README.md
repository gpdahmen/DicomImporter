# DicomImporter

A Python-based GUI application for viewing DICOM (Digital Imaging and Communications in Medicine) medical image files. This application provides an easy-to-use interface for opening and viewing DICOM files along with their metadata.

## Features

- 📁 Open and view DICOM medical image files
- 🖼️ Display DICOM images with automatic scaling
- 📊 View comprehensive DICOM metadata
- 🎨 Clean and intuitive GUI interface
- 💻 Standalone executable - no Python installation required on target PCs

## Requirements

### For Development
- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

### For Running the Executable
- Windows operating system
- No additional software required (all dependencies are bundled)

## Installation and Setup

### Option 1: Running from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gpdahmen/DicomImporter.git
   cd DicomImporter
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Option 2: Building the Executable

To create a standalone `.exe` file that can run on any Windows PC without Python installed:

1. **Ensure dependencies are installed:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the build script:**
   ```bash
   python build.py
   ```

   This script will:
   - Verify PyInstaller is installed
   - Clean previous build artifacts
   - Compile the application using PyInstaller with the following options:
     - `--onefile`: Creates a single executable file
     - `--noconsole`: Prevents a console window from appearing
   - Generate `DicomImporter.exe` in the `dist` directory

3. **Locate the executable:**
   After successful build, the executable will be at:
   ```
   dist/DicomImporter.exe
   ```

### Option 3: Manual PyInstaller Build

If you prefer to build manually:

```bash
pyinstaller --onefile --noconsole --name=DicomImporter main.py
```

## Usage

### Running the Application

**From source:**
```bash
python main.py
```

**From executable:**
Simply double-click `DicomImporter.exe` or run from command line:
```bash
dist\DicomImporter.exe
```

### Using the Application

1. **Open a DICOM file:**
   - Click "Open DICOM File" button or use File → Open DICOM File menu
   - Select a `.dcm` file from your system

2. **View the image:**
   - The "Image Viewer" tab displays the medical image
   - Images are automatically scaled to fit the window

3. **View metadata:**
   - Switch to the "Metadata" tab to see all DICOM tags and values
   - Includes patient information, study details, and technical parameters

## Distribution

To distribute the application to other Windows PCs:

1. Build the executable using `python build.py`
2. Copy `dist/DicomImporter.exe` to the target PC
3. Run the executable - no installation required!

**Note:** The executable is self-contained and includes all necessary dependencies (Python runtime, pydicom, Pillow, numpy, etc.). No additional installations are needed on the target PC.

## Project Structure

```
DicomImporter/
├── main.py              # Main application entry point
├── build.py             # Automated build script for PyInstaller
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore rules
├── build/              # Temporary build files (not in repo)
└── dist/               # Compiled executable output (not in repo)
```

## Dependencies

The application uses the following Python packages:

- **pydicom** (≥2.4.0): For reading and parsing DICOM files
- **Pillow** (≥10.0.0): For image processing and display
- **numpy** (≥1.24.0): For numerical operations on image data
- **pyinstaller** (≥6.0.0): For building the standalone executable

All dependencies are automatically included in the built executable.

## Troubleshooting

### Build Issues

**Problem:** PyInstaller not found
```bash
pip install pyinstaller
```

**Problem:** Missing dependencies during build
```bash
pip install -r requirements.txt
```

**Problem:** Build fails with import errors
- Ensure all dependencies are installed
- Try cleaning build artifacts: delete `build/`, `dist/`, and `*.spec` files
- Run `python build.py` again

### Runtime Issues

**Problem:** Executable doesn't start
- Ensure you're running on a compatible Windows version
- Check Windows Defender or antivirus isn't blocking the executable

**Problem:** "Failed to load DICOM file"
- Ensure the file is a valid DICOM format
- Check file permissions

## Development

### Running Tests
Currently, this project focuses on functionality. To test:
1. Run the application: `python main.py`
2. Load a sample DICOM file
3. Verify image display and metadata viewing work correctly

### Making Changes
1. Modify `main.py` as needed
2. Test changes: `python main.py`
3. Rebuild executable: `python build.py`
4. Test the executable

## License

This project is open source. Please check the repository for license details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Author

gpdahmen

## Acknowledgments

- Built with Python and tkinter
- Uses pydicom for DICOM file handling
- Packaged with PyInstaller