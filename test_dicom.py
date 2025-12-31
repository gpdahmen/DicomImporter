"""
DICOM Engine Test Suite

This module contains comprehensive unit tests for the DicomEngine class and related
functionality. It tests import, export, metadata extraction, and pixel data handling.

The test suite uses Python's unittest framework and includes both positive and negative
test cases to ensure robust error handling and correct functionality.

Test Classes:
    TestDicomEngine: Main test class for DicomEngine functionality
    TestDicomCreation: Tests for creating DICOM files from scratch

Dependencies:
    - unittest: Python's built-in testing framework
    - numpy: For pixel data manipulation and testing
    - pydicom: For DICOM file operations
    - tempfile: For creating temporary test files

Usage:
    python -m unittest test_dicom.py
    python test_dicom.py
"""

import unittest
import tempfile
import os
from pathlib import Path
from typing import Optional
import sys

try:
    import numpy as np
    import pydicom
    from pydicom.dataset import FileDataset
except ImportError:
    np = None
    pydicom = None
    FileDataset = None

# Import the DicomEngine class to test
from dicom_engine import DicomEngine


class TestDicomEngine(unittest.TestCase):
    """
    Test suite for the DicomEngine class.
    
    This class contains unit tests for all major functionality of the DicomEngine,
    including file import, export, metadata extraction, and pixel data handling.
    Tests use temporary files to avoid polluting the filesystem.
    
    Attributes:
        temp_dir (str): Temporary directory for test files
        engine (DicomEngine): DicomEngine instance for testing
    
    Methods:
        setUp: Initialize test environment before each test
        tearDown: Clean up test environment after each test
        test_*: Individual test methods
    """
    
    def setUp(self):
        """
        Set up test environment before each test method.
        
        Creates a temporary directory for test files and initializes a fresh
        DicomEngine instance. This ensures each test starts with a clean state.
        
        Called automatically by unittest before each test method.
        """
        # Create a temporary directory for test files
        # This directory will be automatically cleaned up
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a fresh DicomEngine instance for each test
        # This ensures tests don't interfere with each other
        self.engine = DicomEngine()
    
    def tearDown(self):
        """
        Clean up test environment after each test method.
        
        Removes temporary files and directories created during testing.
        This prevents accumulation of test artifacts on the filesystem.
        
        Called automatically by unittest after each test method.
        """
        # Clean up temporary directory and all its contents
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_sample_dicom(self, file_path: str) -> FileDataset:
        """
        Create a sample DICOM file for testing purposes.
        
        This helper method creates a valid DICOM file with sample data that can
        be used in tests. The file includes basic metadata and a small pixel array.
        
        Args:
            file_path (str): Path where the sample DICOM file should be created
        
        Returns:
            FileDataset: The created DICOM dataset object
        
        Note:
            This is a private helper method used by test methods.
        """
        # Create basic file meta information
        file_meta = pydicom.Dataset()
        file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
        
        # Create the main dataset
        ds = FileDataset(
            filename=file_path,
            dataset={},
            file_meta=file_meta,
            preamble=b"\0" * 128
        )
        
        # Set required DICOM tags with test values
        ds.PatientName = "Test^Patient"
        ds.PatientID = "12345"
        ds.StudyDate = "20250101"
        ds.StudyDescription = "Test Study"
        ds.Modality = "CT"
        ds.SeriesDescription = "Test Series"
        
        # Create a small test image (64x64 pixels)
        # Using a gradient pattern for easy verification
        test_image = np.arange(64 * 64, dtype=np.uint16).reshape(64, 64)
        
        # Set image-related tags
        ds.Rows, ds.Columns = test_image.shape
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 0
        
        # Set pixel data
        ds.PixelData = test_image.tobytes()
        
        # Save the file to disk
        ds.save_as(file_path, write_like_original=False)
        
        return ds
    
    def test_initialization(self):
        """
        Test that DicomEngine initializes correctly.
        
        Verifies that a new DicomEngine instance has the expected initial state:
        - No DICOM file loaded (current_dicom is None)
        - Empty metadata dictionary
        
        This ensures the engine starts in a clean, predictable state.
        """
        # Verify initial state is clean
        self.assertIsNone(self.engine.current_dicom, 
                         "Engine should start with no loaded DICOM")
        self.assertEqual(self.engine.metadata, {}, 
                        "Engine should start with empty metadata")
    
    def test_import_valid_dicom(self):
        """
        Test importing a valid DICOM file.
        
        Creates a sample DICOM file and verifies that:
        - The import operation succeeds
        - The DICOM dataset is loaded into the engine
        - Metadata is extracted correctly
        - All expected metadata fields are present
        """
        # Create a sample DICOM file in the temp directory
        test_file = os.path.join(self.temp_dir, "test.dcm")
        self._create_sample_dicom(test_file)
        
        # Attempt to import the file
        success = self.engine.import_dicom(test_file)
        
        # Verify import was successful
        self.assertTrue(success, "Import should succeed for valid DICOM file")
        
        # Verify DICOM dataset was loaded
        self.assertIsNotNone(self.engine.current_dicom, 
                            "Current DICOM should be loaded after import")
        
        # Verify metadata was extracted
        metadata = self.engine.get_metadata()
        self.assertGreater(len(metadata), 0, 
                          "Metadata should be extracted after import")
        
        # Verify specific metadata fields
        self.assertEqual(metadata['PatientName'], "Test^Patient",
                        "Patient name should match test data")
        self.assertEqual(metadata['PatientID'], "12345",
                        "Patient ID should match test data")
        self.assertEqual(metadata['Modality'], "CT",
                        "Modality should match test data")
    
    def test_import_nonexistent_file(self):
        """
        Test importing a file that doesn't exist.
        
        Verifies that attempting to import a non-existent file:
        - Raises FileNotFoundError
        - Provides an appropriate error message
        
        This ensures proper error handling for invalid file paths.
        """
        # Try to import a file that doesn't exist
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.dcm")
        
        # Verify that FileNotFoundError is raised
        with self.assertRaises(FileNotFoundError):
            self.engine.import_dicom(nonexistent_file)
    
    def test_get_metadata_without_import(self):
        """
        Test getting metadata when no file has been imported.
        
        Verifies that calling get_metadata() on a newly initialized engine
        returns an empty dictionary rather than causing an error.
        
        This ensures safe handling of the "no file loaded" state.
        """
        # Get metadata without importing a file first
        metadata = self.engine.get_metadata()
        
        # Verify empty metadata is returned
        self.assertEqual(metadata, {}, 
                        "Should return empty metadata when no file loaded")
    
    def test_get_pixel_data(self):
        """
        Test extracting pixel data from a DICOM file.
        
        Creates a DICOM file with known pixel data and verifies that:
        - Pixel data can be extracted successfully
        - The extracted array has the correct shape
        - The pixel values match the original data
        
        This ensures pixel data handling works correctly.
        """
        # Create a sample DICOM file with known pixel data
        test_file = os.path.join(self.temp_dir, "test.dcm")
        self._create_sample_dicom(test_file)
        
        # Import the file
        self.engine.import_dicom(test_file)
        
        # Get pixel data
        pixel_data = self.engine.get_pixel_data()
        
        # Verify pixel data was retrieved
        self.assertIsNotNone(pixel_data, "Pixel data should be retrieved")
        
        # Verify shape is correct (64x64 as created in _create_sample_dicom)
        self.assertEqual(pixel_data.shape, (64, 64),
                        "Pixel data should have correct shape")
        
        # Verify data type is appropriate
        self.assertTrue(np.issubdtype(pixel_data.dtype, np.integer),
                       "Pixel data should be integer type")
    
    def test_get_pixel_data_without_import(self):
        """
        Test getting pixel data when no file has been imported.
        
        Verifies that calling get_pixel_data() on a newly initialized engine
        returns None rather than causing an error.
        
        This ensures safe handling of the "no file loaded" state.
        """
        # Try to get pixel data without importing a file first
        pixel_data = self.engine.get_pixel_data()
        
        # Verify None is returned
        self.assertIsNone(pixel_data,
                         "Should return None when no file loaded")
    
    def test_export_dicom(self):
        """
        Test exporting a DICOM file.
        
        Creates and imports a DICOM file, exports it to a new location,
        and verifies that:
        - The export operation succeeds
        - The output file is created
        - The exported file is a valid DICOM file
        - The exported data matches the original
        
        This ensures the export functionality works correctly.
        """
        # Create and import a sample DICOM file
        input_file = os.path.join(self.temp_dir, "input.dcm")
        self._create_sample_dicom(input_file)
        self.engine.import_dicom(input_file)
        
        # Define output path
        output_file = os.path.join(self.temp_dir, "output.dcm")
        
        # Export the file
        success = self.engine.export_dicom(output_file)
        
        # Verify export was successful
        self.assertTrue(success, "Export should succeed")
        
        # Verify output file was created
        self.assertTrue(os.path.exists(output_file),
                       "Output file should be created")
        
        # Verify the exported file is a valid DICOM file
        # by attempting to read it
        exported_ds = pydicom.dcmread(output_file)
        self.assertIsNotNone(exported_ds,
                            "Exported file should be valid DICOM")
        
        # Verify key metadata matches
        self.assertEqual(str(exported_ds.PatientName), "Test^Patient",
                        "Exported patient name should match original")
    
    def test_export_without_import(self):
        """
        Test exporting when no file has been imported.
        
        Verifies that attempting to export without loading a file first:
        - Raises ValueError
        - Provides an appropriate error message
        
        This ensures proper error handling for invalid operations.
        """
        # Try to export without importing a file first
        output_file = os.path.join(self.temp_dir, "output.dcm")
        
        # Verify that ValueError is raised
        with self.assertRaises(ValueError):
            self.engine.export_dicom(output_file)
    
    def test_create_dicom_from_array(self):
        """
        Test creating a DICOM file from a numpy array.
        
        Creates a DICOM dataset from a numpy array with custom metadata
        and verifies that:
        - The dataset is created successfully
        - The pixel data matches the input array
        - The metadata is set correctly
        - The file can be exported and read back
        
        This ensures DICOM creation from scratch works correctly.
        """
        # Create a simple test image
        test_image = np.random.randint(0, 1000, (128, 128), dtype=np.uint16)
        
        # Create metadata for the DICOM file
        metadata = {
            'PatientName': 'Created^Patient',
            'PatientID': 'CREATE001',
            'Modality': 'MR'
        }
        
        # Create DICOM dataset from array
        ds = self.engine.create_dicom_from_array(test_image, metadata)
        
        # Verify dataset was created
        self.assertIsNotNone(ds, "Dataset should be created")
        
        # Verify metadata was set correctly
        self.assertEqual(str(ds.PatientName), 'Created^Patient',
                        "Patient name should be set from metadata")
        self.assertEqual(str(ds.PatientID), 'CREATE001',
                        "Patient ID should be set from metadata")
        self.assertEqual(str(ds.Modality), 'MR',
                        "Modality should be set from metadata")
        
        # Verify image dimensions were set correctly
        self.assertEqual(ds.Rows, 128, "Rows should match image shape")
        self.assertEqual(ds.Columns, 128, "Columns should match image shape")
        
        # Export and re-import to verify pixel data
        output_file = os.path.join(self.temp_dir, "created.dcm")
        self.engine.export_dicom(output_file, ds)
        
        # Read back and verify
        reimported_ds = pydicom.dcmread(output_file)
        reimported_pixels = reimported_ds.pixel_array
        
        # Verify pixel data matches (allowing for DICOM encoding/decoding)
        np.testing.assert_array_equal(reimported_pixels, test_image,
                                     "Pixel data should match original array")
    
    def test_list_all_tags(self):
        """
        Test listing all DICOM tags in a file.
        
        Creates and imports a DICOM file and verifies that:
        - The list_all_tags method returns a list
        - The list contains expected tag names
        - Common DICOM tags are present
        
        This ensures tag listing functionality works correctly.
        """
        # Create and import a sample DICOM file
        test_file = os.path.join(self.temp_dir, "test.dcm")
        self._create_sample_dicom(test_file)
        self.engine.import_dicom(test_file)
        
        # Get list of all tags
        tags = self.engine.list_all_tags()
        
        # Verify tags were retrieved
        self.assertIsInstance(tags, list, "Should return a list")
        self.assertGreater(len(tags), 0, "Should return non-empty list")
        
        # Verify some common tags are present
        self.assertIn('PatientName', tags, "PatientName tag should be present")
        self.assertIn('Modality', tags, "Modality tag should be present")
    
    def test_list_all_tags_without_import(self):
        """
        Test listing tags when no file has been imported.
        
        Verifies that calling list_all_tags() on a newly initialized engine
        returns an empty list rather than causing an error.
        
        This ensures safe handling of the "no file loaded" state.
        """
        # Try to list tags without importing a file first
        tags = self.engine.list_all_tags()
        
        # Verify empty list is returned
        self.assertEqual(tags, [], "Should return empty list when no file loaded")


def run_tests():
    """
    Run the test suite and display results.
    
    This function runs all tests in the TestDicomEngine class and displays
    a summary of results. It's the main entry point when running tests directly.
    
    Returns:
        int: 0 if all tests passed, 1 if any tests failed
    
    Example:
        >>> exit_code = run_tests()
        >>> sys.exit(exit_code)
    """
    # Check if required dependencies are available
    if np is None or pydicom is None:
        print("=" * 70)
        print("ERROR: Required test dependencies not installed")
        print("=" * 70)
        print("\nPlease install required packages:")
        print("  pip install pydicom numpy")
        print()
        return 1
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDicomEngine)
    
    # Run the tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1


# Entry point when script is run directly
if __name__ == '__main__':
    sys.exit(run_tests())
