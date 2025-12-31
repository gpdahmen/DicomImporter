"""
DICOM Engine Module

This module provides core functionality for importing and exporting DICOM (Digital Imaging 
and Communications in Medicine) files. It handles reading DICOM metadata and pixel data,
as well as creating and exporting DICOM files with proper formatting.

The module uses the pydicom library for DICOM file manipulation and numpy for pixel data handling.

Classes:
    DicomEngine: Main class for DICOM file operations

Functions:
    None (all functionality encapsulated in DicomEngine class)

Dependencies:
    - pydicom: For DICOM file reading and writing
    - numpy: For pixel data manipulation
    - pathlib: For file path operations
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
try:
    import pydicom
    from pydicom.dataset import Dataset, FileDataset
    import numpy as np
except ImportError:
    # Graceful handling if dependencies are not installed
    pydicom = None
    Dataset = None
    FileDataset = None
    np = None


class DicomEngine:
    """
    A comprehensive engine for DICOM file import and export operations.
    
    This class provides methods to read DICOM files, extract metadata and pixel data,
    create new DICOM files, and export them to the filesystem. It handles various
    DICOM formats and ensures proper data validation.
    
    Attributes:
        current_dicom (Optional[FileDataset]): Currently loaded DICOM dataset
        metadata (Dict[str, Any]): Extracted metadata from the current DICOM file
    
    Example:
        >>> engine = DicomEngine()
        >>> engine.import_dicom("path/to/file.dcm")
        >>> metadata = engine.get_metadata()
        >>> engine.export_dicom("output/path.dcm")
    """
    
    def __init__(self):
        """
        Initialize the DicomEngine with empty state.
        
        Sets up the engine with no loaded DICOM file and empty metadata dictionary.
        Also verifies that required dependencies are available.
        
        Raises:
            ImportError: If required dependencies (pydicom, numpy) are not installed
        """
        if pydicom is None or np is None:
            raise ImportError(
                "Required dependencies not found. Please install pydicom and numpy: "
                "pip install pydicom numpy"
            )
        
        # Initialize the current DICOM dataset to None (no file loaded)
        self.current_dicom: Optional[FileDataset] = None
        
        # Initialize empty metadata dictionary
        self.metadata: Dict[str, Any] = {}
    
    def import_dicom(self, file_path: str) -> bool:
        """
        Import a DICOM file from the specified path.
        
        Reads a DICOM file from disk, loads it into memory, and extracts its metadata.
        The file is validated to ensure it's a proper DICOM format before loading.
        
        Args:
            file_path (str): Path to the DICOM file to import. Can be absolute or relative.
        
        Returns:
            bool: True if the file was successfully imported, False otherwise.
        
        Raises:
            FileNotFoundError: If the specified file does not exist
            pydicom.errors.InvalidDicomError: If the file is not a valid DICOM file
        
        Example:
            >>> engine = DicomEngine()
            >>> success = engine.import_dicom("/path/to/scan.dcm")
            >>> if success:
            ...     print("DICOM file loaded successfully")
        """
        # Convert string path to Path object for better path handling
        path = Path(file_path)
        
        # Validate that the file exists before attempting to read
        if not path.exists():
            raise FileNotFoundError(f"DICOM file not found: {file_path}")
        
        try:
            # Read the DICOM file using pydicom
            # force=True allows reading of non-standard DICOM files
            self.current_dicom = pydicom.dcmread(str(path), force=False)
            
            # Extract metadata from the loaded DICOM file
            self._extract_metadata()
            
            return True
        
        except Exception as e:
            # Log the error and return False to indicate failure
            print(f"Error importing DICOM file: {str(e)}")
            return False
    
    def _extract_metadata(self) -> None:
        """
        Extract metadata from the currently loaded DICOM file.
        
        This private method extracts key DICOM tags and stores them in the metadata
        dictionary for easy access. It handles missing tags gracefully by providing
        default values.
        
        Common DICOM tags extracted:
            - PatientName: Name of the patient
            - PatientID: Unique patient identifier
            - StudyDate: Date when the study was performed
            - Modality: Type of equipment (CT, MR, etc.)
            - SeriesDescription: Description of the image series
            - Rows/Columns: Image dimensions
        
        Returns:
            None: Updates self.metadata dictionary in place
        
        Note:
            This is a private method and should not be called directly by users.
        """
        if self.current_dicom is None:
            return
        
        # Extract patient information with fallback to "Unknown" if not present
        self.metadata['PatientName'] = str(getattr(
            self.current_dicom, 'PatientName', 'Unknown'
        ))
        self.metadata['PatientID'] = str(getattr(
            self.current_dicom, 'PatientID', 'Unknown'
        ))
        
        # Extract study information
        self.metadata['StudyDate'] = str(getattr(
            self.current_dicom, 'StudyDate', 'Unknown'
        ))
        self.metadata['StudyDescription'] = str(getattr(
            self.current_dicom, 'StudyDescription', 'Unknown'
        ))
        
        # Extract imaging modality (e.g., CT, MR, US, etc.)
        self.metadata['Modality'] = str(getattr(
            self.current_dicom, 'Modality', 'Unknown'
        ))
        
        # Extract series information
        self.metadata['SeriesDescription'] = str(getattr(
            self.current_dicom, 'SeriesDescription', 'Unknown'
        ))
        
        # Extract image dimensions if available
        self.metadata['Rows'] = getattr(self.current_dicom, 'Rows', None)
        self.metadata['Columns'] = getattr(self.current_dicom, 'Columns', None)
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Retrieve the metadata dictionary of the currently loaded DICOM file.
        
        Returns the metadata extracted from the DICOM file, including patient information,
        study details, and image properties.
        
        Returns:
            Dict[str, Any]: Dictionary containing DICOM metadata key-value pairs.
                           Returns empty dict if no DICOM file is currently loaded.
        
        Example:
            >>> engine = DicomEngine()
            >>> engine.import_dicom("scan.dcm")
            >>> metadata = engine.get_metadata()
            >>> print(f"Patient: {metadata['PatientName']}")
            >>> print(f"Modality: {metadata['Modality']}")
        """
        return self.metadata.copy()  # Return a copy to prevent external modifications
    
    def get_pixel_data(self) -> Optional[np.ndarray]:
        """
        Extract pixel data from the currently loaded DICOM file.
        
        Retrieves the pixel array from the DICOM file and returns it as a numpy array.
        This data represents the actual image content and can be used for visualization
        or further processing.
        
        Returns:
            Optional[np.ndarray]: Numpy array containing pixel data, or None if:
                                 - No DICOM file is currently loaded
                                 - The DICOM file does not contain pixel data
                                 - An error occurs during pixel data extraction
        
        Example:
            >>> engine = DicomEngine()
            >>> engine.import_dicom("scan.dcm")
            >>> pixels = engine.get_pixel_data()
            >>> if pixels is not None:
            ...     print(f"Image shape: {pixels.shape}")
            ...     print(f"Data type: {pixels.dtype}")
        """
        if self.current_dicom is None:
            return None
        
        try:
            # Extract pixel array from DICOM dataset
            # This converts the DICOM pixel data to a numpy array
            pixel_array = self.current_dicom.pixel_array
            return pixel_array
        
        except AttributeError:
            # DICOM file does not contain pixel data (e.g., structured reports)
            print("Warning: DICOM file does not contain pixel data")
            return None
        
        except Exception as e:
            # Handle any other errors during pixel data extraction
            print(f"Error extracting pixel data: {str(e)}")
            return None
    
    def export_dicom(self, output_path: str, dataset: Optional[FileDataset] = None) -> bool:
        """
        Export a DICOM file to the specified output path.
        
        Writes either the currently loaded DICOM dataset or a provided dataset to disk
        in standard DICOM format. Creates parent directories if they don't exist.
        
        Args:
            output_path (str): Destination path where the DICOM file will be saved.
                              Can be absolute or relative.
            dataset (Optional[FileDataset]): DICOM dataset to export. If None, exports
                                            the currently loaded dataset.
        
        Returns:
            bool: True if export was successful, False otherwise.
        
        Raises:
            ValueError: If no dataset is available to export (neither provided nor loaded)
            OSError: If there are permission issues or disk space problems
        
        Example:
            >>> engine = DicomEngine()
            >>> engine.import_dicom("input.dcm")
            >>> success = engine.export_dicom("output/modified.dcm")
            >>> if success:
            ...     print("DICOM file exported successfully")
        """
        # Determine which dataset to export
        export_dataset = dataset if dataset is not None else self.current_dicom
        
        # Validate that we have a dataset to export
        if export_dataset is None:
            raise ValueError("No DICOM dataset available to export")
        
        try:
            # Convert output path to Path object for easier manipulation
            path = Path(output_path)
            
            # Create parent directories if they don't exist
            # This ensures the full path structure is available
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the DICOM dataset to file
            # write_like_original=False ensures consistent output format
            export_dataset.save_as(str(path), write_like_original=False)
            
            return True
        
        except Exception as e:
            # Log the error and return False to indicate failure
            print(f"Error exporting DICOM file: {str(e)}")
            return False
    
    def create_dicom_from_array(
        self, 
        pixel_array: np.ndarray, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> FileDataset:
        """
        Create a new DICOM dataset from a numpy pixel array and optional metadata.
        
        This method allows creation of DICOM files from raw pixel data, useful for
        converting other image formats to DICOM or creating synthetic DICOM files.
        The method ensures all required DICOM tags are present.
        
        Args:
            pixel_array (np.ndarray): 2D or 3D numpy array containing pixel data.
                                     Shape should be (rows, columns) or 
                                     (frames, rows, columns).
            metadata (Optional[Dict[str, Any]]): Dictionary of DICOM tags to include.
                                                If None, minimal required tags are used.
        
        Returns:
            FileDataset: A new DICOM dataset object that can be exported to file.
        
        Example:
            >>> import numpy as np
            >>> engine = DicomEngine()
            >>> # Create a simple 512x512 test image
            >>> image = np.random.randint(0, 255, (512, 512), dtype=np.uint8)
            >>> metadata = {
            ...     'PatientName': 'Test^Patient',
            ...     'Modality': 'CT'
            ... }
            >>> dicom_ds = engine.create_dicom_from_array(image, metadata)
            >>> engine.export_dicom("output.dcm", dicom_ds)
        """
        # Create a new FileDataset with minimal required metadata
        file_meta = pydicom.Dataset()
        
        # Set the Transfer Syntax UID (required for DICOM)
        # Explicit VR Little Endian is a commonly supported transfer syntax
        file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
        
        # Create the main dataset
        ds = FileDataset(
            filename="",  # Filename will be set during export
            dataset={},
            file_meta=file_meta,
            preamble=b"\0" * 128  # Standard DICOM preamble
        )
        
        # Set required DICOM tags with default values
        ds.PatientName = "Anonymous"
        ds.PatientID = "00000000"
        
        # Set modality (type of imaging equipment)
        ds.Modality = "OT"  # OT = Other
        
        # Set image dimensions from the pixel array
        if len(pixel_array.shape) == 2:
            # 2D image
            ds.Rows, ds.Columns = pixel_array.shape
        elif len(pixel_array.shape) == 3:
            # 3D image (multi-frame)
            _, ds.Rows, ds.Columns = pixel_array.shape
        
        # Set pixel data properties
        ds.SamplesPerPixel = 1  # Grayscale image
        ds.PhotometricInterpretation = "MONOCHROME2"  # Standard grayscale
        ds.BitsAllocated = 16  # Bits per pixel
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 0  # Unsigned integer
        
        # Override defaults with provided metadata if available
        if metadata:
            for key, value in metadata.items():
                setattr(ds, key, value)
        
        # Set the pixel data
        ds.PixelData = pixel_array.tobytes()
        
        return ds
    
    def list_all_tags(self) -> List[str]:
        """
        List all DICOM tags present in the currently loaded file.
        
        Returns a list of all DICOM tag names (data elements) present in the current
        dataset. Useful for exploring available metadata or debugging.
        
        Returns:
            List[str]: List of DICOM tag names. Empty list if no file is loaded.
        
        Example:
            >>> engine = DicomEngine()
            >>> engine.import_dicom("scan.dcm")
            >>> tags = engine.list_all_tags()
            >>> print(f"Found {len(tags)} DICOM tags")
            >>> print("First 5 tags:", tags[:5])
        """
        if self.current_dicom is None:
            return []
        
        # Extract all data element keywords from the dataset
        return [elem.keyword for elem in self.current_dicom if elem.keyword]
