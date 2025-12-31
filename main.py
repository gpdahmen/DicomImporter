#!/usr/bin/env python3
"""
DICOM Importer - A simple GUI application for importing and viewing DICOM medical images.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys


class DicomImporterApp:
    """Main application class for DICOM Importer."""
    
    # Class constant for DICOM file extensions
    DICOM_EXTENSIONS = ['.dcm', '.dicom', '.dic']
    
    def __init__(self, root):
        """Initialize the DICOM Importer application.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("DICOM Importer")
        self.root.geometry("600x400")
        
        # Set minimum window size
        self.root.minsize(500, 300)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title label
        title_label = ttk.Label(
            main_frame, 
            text="DICOM Importer", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=10)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)
        
        # Import button
        self.import_button = ttk.Button(
            button_frame,
            text="Import DICOM File",
            command=self.import_dicom_file
        )
        self.import_button.pack(side=tk.LEFT, padx=5)
        
        # Import folder button
        self.import_folder_button = ttk.Button(
            button_frame,
            text="Import DICOM Folder",
            command=self.import_dicom_folder
        )
        self.import_folder_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_button = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_list
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Text area with scrollbar for displaying imported files
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Text widget
        self.text_area = tk.Text(
            text_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED,
            height=15
        )
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.text_area.yview)
        
        # Status bar
        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Initialize file counter
        self.file_count = 0
        
        # Add initial welcome message
        self.append_text("Welcome to DICOM Importer!\n")
        self.append_text("Click 'Import DICOM File' or 'Import DICOM Folder' to get started.\n")
        self.append_text("-" * 60 + "\n")
    
    def append_text(self, text):
        """Append text to the text area.
        
        Args:
            text: The text to append
        """
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
    
    def clear_list(self):
        """Clear the text area."""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.file_count = 0
        self.update_status("Cleared")
    
    def update_status(self, message):
        """Update the status bar.
        
        Args:
            message: The status message to display
        """
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def is_dicom_file(self, filepath):
        """Check if a file is potentially a DICOM file.
        
        Args:
            filepath: Path to the file to check
            
        Returns:
            bool: True if file might be DICOM, False otherwise
        """
        # Check common DICOM extensions
        _, ext = os.path.splitext(filepath.lower())
        
        if ext in self.DICOM_EXTENSIONS:
            return True
        
        # DICOM files can have no extension, so check if it's a file
        if os.path.isfile(filepath) and not ext:
            return True
            
        return False
    
    def import_dicom_file(self):
        """Import a single DICOM file."""
        self.update_status("Selecting file...")
        
        filepath = filedialog.askopenfilename(
            title="Select DICOM File",
            filetypes=[
                ("DICOM files", "*.dcm *.dicom *.dic"),
                ("All files", "*.*")
            ]
        )
        
        if filepath:
            self.process_dicom_file(filepath)
            self.update_status(f"Imported 1 file")
        else:
            self.update_status("No file selected")
    
    def import_dicom_folder(self):
        """Import all DICOM files from a folder."""
        self.update_status("Selecting folder...")
        
        folder_path = filedialog.askdirectory(title="Select DICOM Folder")
        
        if folder_path:
            imported_count = 0
            self.append_text(f"\nScanning folder: {folder_path}\n")
            
            # Walk through directory and subdirectories
            # Update UI periodically to maintain responsiveness
            file_batch = []
            batch_size = 10  # Process files in batches
            
            for root_dir, _, files in os.walk(folder_path):
                for filename in files:
                    filepath = os.path.join(root_dir, filename)
                    if self.is_dicom_file(filepath):
                        file_batch.append(filepath)
                        
                        # Process batch when it reaches the batch size
                        if len(file_batch) >= batch_size:
                            for file_path in file_batch:
                                self.process_dicom_file(file_path)
                                imported_count += 1
                            file_batch = []
                            # Update UI to prevent blocking
                            self.root.update_idletasks()
                            self.update_status(f"Processing... ({imported_count} files)")
            
            # Process remaining files in the last batch
            for file_path in file_batch:
                self.process_dicom_file(file_path)
                imported_count += 1
            
            if imported_count > 0:
                self.append_text(f"\nTotal files imported from folder: {imported_count}\n")
                self.append_text("-" * 60 + "\n")
                self.update_status(f"Imported {imported_count} file(s) from folder")
            else:
                self.append_text("No DICOM files found in the selected folder.\n")
                self.update_status("No DICOM files found")
        else:
            self.update_status("No folder selected")
    
    def process_dicom_file(self, filepath):
        """Process and display information about a DICOM file.
        
        Args:
            filepath: Path to the DICOM file
        """
        try:
            self.file_count += 1
            filename = os.path.basename(filepath)
            file_size = os.path.getsize(filepath)
            
            # Format file size
            size_str = self.format_file_size(file_size)
            
            # Display file information
            self.append_text(f"\n[{self.file_count}] {filename}\n")
            self.append_text(f"    Path: {filepath}\n")
            self.append_text(f"    Size: {size_str}\n")
            
        except Exception as e:
            self.append_text(f"\nError processing {filepath}: {str(e)}\n")
            messagebox.showerror("Error", f"Failed to process file:\n{filepath}\n\nError: {str(e)}")
    
    @staticmethod
    def format_file_size(size_bytes):
        """Format file size in human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            str: Formatted file size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = DicomImporterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
