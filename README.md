# DicomImporter

A DICOM file importer/exporter application with a user-friendly GUI built using Python.

## CI/CD Pipeline

This repository includes a GitHub Actions workflow that automatically builds a standalone Windows executable (`.exe`) file from the Python project.

### How the Workflow Works

The workflow (`build-exe.yml`) is triggered automatically:
- **On push** to the `main` branch
- **On pull request** creation targeting the `main` branch

The workflow performs the following steps:

1. **Checkout the repository** - Retrieves the latest code
2. **Set up Python** - Installs Python 3.11 on a Windows runner
3. **Install dependencies** - Installs PyInstaller and all dependencies from `requirements.txt`
4. **Build the executable** - Uses PyInstaller to create a single `.exe` file from `main.py`
5. **Upload artifact** - Saves the generated `.exe` file as a downloadable artifact

### Downloading the Executable

After a successful workflow run, you can download the executable:

1. Navigate to the [Actions](../../actions) tab in the repository
2. Click on the latest successful workflow run (indicated by a green checkmark ✓)
3. Scroll down to the **Artifacts** section
4. Download the `DicomImporter-exe` artifact (ZIP file)
5. Extract the ZIP file to access the `DicomImporter.exe` file

The artifacts are retained for 90 days and are available as ZIP files containing the executable.

### Building Locally

To build the executable locally on Windows:

```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build the executable
pyinstaller --onefile --windowed --name DicomImporter main.py

# The executable will be in the dist/ folder
```

## Usage

For detailed usage instructions, please refer to the application documentation.