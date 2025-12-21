"""
Test suite for DICOM Import/Export Application

This module tests the core functionality of the DicomEngine.
"""

import os
import tempfile
import shutil
from dicom_engine import DicomEngine


def test_is_dicom():
    """Test the is_dicom method with valid and invalid files."""
    print("Testing is_dicom method...")
    
    engine = DicomEngine()
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Test 1: Valid DICOM file
        valid_dicom = os.path.join(temp_dir, "valid.dcm")
        with open(valid_dicom, 'wb') as f:
            # Write 128 byte preamble
            f.write(b'\x00' * 128)
            # Write DICM magic bytes
            f.write(b'DICM')
            # Write some dummy data
            f.write(b'dummy data')
        
        assert engine.is_dicom(valid_dicom), "Valid DICOM file should be detected"
        print("✓ Valid DICOM file detected correctly")
        
        # Test 2: Invalid DICOM file (no DICM magic)
        invalid_dicom = os.path.join(temp_dir, "invalid.dcm")
        with open(invalid_dicom, 'wb') as f:
            f.write(b'\x00' * 128)
            f.write(b'ABCD')  # Wrong magic bytes
        
        assert not engine.is_dicom(invalid_dicom), "Invalid DICOM file should not be detected"
        print("✓ Invalid DICOM file rejected correctly")
        
        # Test 3: Non-DICOM file
        text_file = os.path.join(temp_dir, "text.txt")
        with open(text_file, 'w') as f:
            f.write("This is not a DICOM file")
        
        assert not engine.is_dicom(text_file), "Text file should not be detected as DICOM"
        print("✓ Text file rejected correctly")
        
        # Test 4: File too small
        small_file = os.path.join(temp_dir, "small.dcm")
        with open(small_file, 'wb') as f:
            f.write(b'small')
        
        assert not engine.is_dicom(small_file), "File too small should not be detected as DICOM"
        print("✓ Small file rejected correctly")
        
        print("\n✓ All is_dicom tests passed!")
        return True
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def test_cache_files():
    """Test the cache_files method."""
    print("\nTesting cache_files method...")
    
    messages = []
    def log_callback(msg):
        messages.append(msg)
    
    engine = DicomEngine(log_callback=log_callback)
    
    # Create temporary source directory with test files
    source_dir = tempfile.mkdtemp()
    
    try:
        # Create some valid DICOM files
        for i in range(3):
            dicom_file = os.path.join(source_dir, f"dicom_{i}.dcm")
            with open(dicom_file, 'wb') as f:
                f.write(b'\x00' * 128)
                f.write(b'DICM')
                f.write(b'test data')
        
        # Create some non-DICOM files
        text_file = os.path.join(source_dir, "readme.txt")
        with open(text_file, 'w') as f:
            f.write("Not a DICOM file")
        
        # Create subdirectory with DICOM file
        sub_dir = os.path.join(source_dir, "subdir")
        os.makedirs(sub_dir)
        sub_dicom = os.path.join(sub_dir, "sub_dicom.dcm")
        with open(sub_dicom, 'wb') as f:
            f.write(b'\x00' * 128)
            f.write(b'DICM')
            f.write(b'sub data')
        
        # Cache files
        cached_count, total_count = engine.cache_files(source_dir)
        
        assert cached_count == 4, f"Expected 4 cached files, got {cached_count}"
        assert total_count == 5, f"Expected 5 total files, got {total_count}"
        assert len(engine.cached_files) == 4, f"Expected 4 files in cache list, got {len(engine.cached_files)}"
        
        # Verify cached files exist
        for cached_file in engine.cached_files:
            assert os.path.exists(cached_file), f"Cached file {cached_file} should exist"
            assert engine.is_dicom(cached_file), f"Cached file {cached_file} should be valid DICOM"
        
        print(f"✓ Cached {cached_count} DICOM files out of {total_count} total files")
        print(f"✓ Cache directory: {engine.cache_dir}")
        
        # Save cache dir path before cleanup
        cache_dir_path = engine.cache_dir
        
        # Cleanup
        engine.cleanup()
        assert not os.path.exists(cache_dir_path), "Cache directory should be cleaned up"
        print("✓ Cache cleanup successful")
        
        print("\n✓ All cache_files tests passed!")
        return True
        
    finally:
        # Cleanup source directory
        shutil.rmtree(source_dir)


def test_send_to_folder():
    """Test the send_to_folder method."""
    print("\nTesting send_to_folder method...")
    
    engine = DicomEngine()
    
    # Create temporary source directory
    source_dir = tempfile.mkdtemp()
    dest_dir = tempfile.mkdtemp()
    
    try:
        # Create some DICOM files
        for i in range(2):
            dicom_file = os.path.join(source_dir, f"test_{i}.dcm")
            with open(dicom_file, 'wb') as f:
                f.write(b'\x00' * 128)
                f.write(b'DICM')
                f.write(f'data {i}'.encode())
        
        # Cache files
        cached_count, _ = engine.cache_files(source_dir)
        assert cached_count == 2, f"Expected 2 cached files, got {cached_count}"
        
        # Send to folder
        copied_count = engine.send_to_folder(dest_dir)
        assert copied_count == 2, f"Expected 2 copied files, got {copied_count}"
        
        # Verify files in destination
        dest_files = os.listdir(dest_dir)
        assert len(dest_files) == 2, f"Expected 2 files in destination, got {len(dest_files)}"
        
        for dest_file in dest_files:
            dest_path = os.path.join(dest_dir, dest_file)
            assert engine.is_dicom(dest_path), f"Destination file {dest_file} should be valid DICOM"
        
        print(f"✓ Copied {copied_count} files to destination folder")
        print(f"✓ Destination: {dest_dir}")
        
        # Cleanup
        engine.cleanup()
        
        print("\n✓ All send_to_folder tests passed!")
        return True
        
    finally:
        # Cleanup
        shutil.rmtree(source_dir)
        shutil.rmtree(dest_dir)


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("DICOM Import/Export Application - Test Suite")
    print("="*60)
    
    tests = [
        test_is_dicom,
        test_cache_files,
        test_send_to_folder,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n✗ Test failed: {test.__name__}")
            print(f"  Error: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
