"""
DicomEngine - Core business logic for DICOM file operations.

This module handles all file operations and PACS communication,
designed to be UI-agnostic.
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Callable, Optional

import pydicom
from pynetdicom import AE, Association
from pynetdicom.sop_class import (
    CTImageStorage,
    MRImageStorage,
    SecondaryCaptureImageStorage,
    DigitalXRayImageStorageForPresentation,
    ComputedRadiographyImageStorage,
    UltrasoundImageStorage,
    UltrasoundMultiFrameImageStorage,
    XRayAngiographicImageStorage,
    PositronEmissionTomographyImageStorage,
    RTImageStorage,
)


class DicomEngine:
    """
    Handles DICOM file operations including caching, folder export, and PACS export.
    """

    def __init__(self, log_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize the DicomEngine.

        Args:
            log_callback: Optional callback function for logging messages.
        """
        self.log_callback = log_callback
        self.cache_dir: Optional[str] = None
        self.cached_files: list[str] = []

    def _log(self, message: str) -> None:
        """
        Log a message using the callback if available.

        Args:
            message: The message to log.
        """
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def is_dicom(self, filepath: str) -> bool:
        """
        Check if a file is a valid DICOM file by verifying the DICM header.

        This method performs a lightweight check by reading the specific "DICM"
        header signature at byte offset 128.

        Args:
            filepath: Path to the file to check.

        Returns:
            True if the file has a valid DICM header, False otherwise.
        """
        try:
            with open(filepath, 'rb') as f:
                # Skip the 128-byte preamble
                f.seek(128)
                # Read the 4-byte DICOM prefix
                magic = f.read(4)
                return magic == b'DICM'
        except Exception:
            return False

    def cache_files(
        self,
        source_dir: str,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> tuple[int, int]:
        """
        Cache DICOM files from source directory to temporary local storage.

        This method recursively scans the source directory and copies all valid
        DICOM files to a temporary cache. This is especially useful for optical
        media (CD/DVD) where sequential reading is much faster than random access.

        Args:
            source_dir: Source directory to scan for DICOM files.
            progress_callback: Optional callback function(current, total) for progress updates.

        Returns:
            Tuple of (files_cached, total_files_found).
        """
        # Create temporary cache directory
        self.cache_dir = tempfile.mkdtemp(prefix='dicom_cache_')
        self._log(f"Created cache directory: {self.cache_dir}")

        # First pass: count all files
        self._log(f"Scanning source directory: {source_dir}")
        all_files = []
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                filepath = os.path.join(root, file)
                all_files.append(filepath)

        total_files = len(all_files)
        self._log(f"Found {total_files} files to check")

        # Second pass: cache valid DICOM files
        cached_count = 0
        self.cached_files = []

        for idx, filepath in enumerate(all_files, 1):
            if self.is_dicom(filepath):
                try:
                    # Create a unique filename in cache
                    cache_filename = f"dicom_{cached_count:06d}.dcm"
                    cache_path = os.path.join(self.cache_dir, cache_filename)

                    # Copy file to cache
                    shutil.copy2(filepath, cache_path)
                    self.cached_files.append(cache_path)
                    cached_count += 1

                    self._log(f"Cached: {os.path.basename(filepath)} ({cached_count}/{total_files})")
                except Exception as e:
                    self._log(f"Error caching {filepath}: {str(e)}")

            # Update progress
            if progress_callback:
                progress_callback(idx, total_files)

        self._log(f"Caching complete: {cached_count} DICOM files cached")
        return cached_count, total_files

    def send_to_folder(
        self,
        destination_folder: str,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> int:
        """
        Copy cached DICOM files to a destination folder.

        Args:
            destination_folder: Target folder for DICOM files.
            progress_callback: Optional callback function(current, total) for progress updates.

        Returns:
            Number of files successfully copied.
        """
        if not self.cached_files:
            self._log("No cached files to export")
            return 0

        # Create destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)
        self._log(f"Exporting to folder: {destination_folder}")

        copied_count = 0
        total = len(self.cached_files)

        for idx, cached_file in enumerate(self.cached_files, 1):
            try:
                filename = f"export_{idx:06d}.dcm"
                dest_path = os.path.join(destination_folder, filename)
                shutil.copy2(cached_file, dest_path)
                copied_count += 1
                self._log(f"Copied: {filename} ({idx}/{total})")

                if progress_callback:
                    progress_callback(idx, total)
            except Exception as e:
                self._log(f"Error copying {cached_file}: {str(e)}")

        self._log(f"Export complete: {copied_count} files copied")
        return copied_count

    def send_to_pacs(
        self,
        ae_title: str,
        pacs_ip: str,
        pacs_port: int,
        called_ae_title: str = "ANY-SCP",
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> int:
        """
        Send cached DICOM files to a PACS server using C-STORE.

        Args:
            ae_title: Application Entity title for this application.
            pacs_ip: IP address of the PACS server.
            pacs_port: Port number of the PACS server.
            called_ae_title: AE Title of the PACS server (default: "ANY-SCP").
            progress_callback: Optional callback function(current, total) for progress updates.

        Returns:
            Number of files successfully sent.
        """
        if not self.cached_files:
            self._log("No cached files to send")
            return 0

        # Initialize Application Entity
        ae = AE(ae_title=ae_title)

        # Add presentation contexts for common DICOM storage SOP classes
        ae.add_requested_context(CTImageStorage)
        ae.add_requested_context(MRImageStorage)
        ae.add_requested_context(SecondaryCaptureImageStorage)
        ae.add_requested_context(DigitalXRayImageStorageForPresentation)
        ae.add_requested_context(ComputedRadiographyImageStorage)
        ae.add_requested_context(UltrasoundImageStorage)
        ae.add_requested_context(UltrasoundMultiFrameImageStorage)
        ae.add_requested_context(XRayAngiographicImageStorage)
        ae.add_requested_context(PositronEmissionTomographyImageStorage)
        ae.add_requested_context(RTImageStorage)

        self._log(f"Connecting to PACS: {pacs_ip}:{pacs_port} (AE: {called_ae_title})")

        try:
            # Establish association with PACS
            assoc = ae.associate(pacs_ip, pacs_port, ae_title=called_ae_title)

            if not assoc.is_established:
                self._log("Failed to establish association with PACS")
                return 0

            self._log("Association established")

            sent_count = 0
            total = len(self.cached_files)

            for idx, cached_file in enumerate(self.cached_files, 1):
                try:
                    # Read DICOM file
                    ds = pydicom.dcmread(cached_file)

                    # Send C-STORE request
                    status = assoc.send_c_store(ds)

                    if status and status.Status == 0x0000:
                        sent_count += 1
                        self._log(f"Sent: {os.path.basename(cached_file)} ({idx}/{total})")
                    else:
                        self._log(f"Failed to send {cached_file}: Status {status.Status if status else 'None'}")

                    if progress_callback:
                        progress_callback(idx, total)
                except Exception as e:
                    self._log(f"Error sending {cached_file}: {str(e)}")

            # Release association
            assoc.release()
            self._log(f"PACS export complete: {sent_count} files sent")
            return sent_count

        except Exception as e:
            self._log(f"PACS connection error: {str(e)}")
            return 0

    def cleanup(self) -> None:
        """
        Clean up temporary cache directory and files.
        """
        if self.cache_dir and os.path.exists(self.cache_dir):
            try:
                shutil.rmtree(self.cache_dir)
                self._log(f"Cleaned up cache directory: {self.cache_dir}")
            except Exception as e:
                self._log(f"Error cleaning up cache: {str(e)}")

        self.cache_dir = None
        self.cached_files = []
