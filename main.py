#!/usr/bin/env python3
"""
DICOM Importer - A GUI application for viewing DICOM medical image files
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys

try:
    import pydicom
    from PIL import Image, ImageTk
    import numpy as np
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Please install required dependencies: pip install -r requirements.txt")
    sys.exit(1)


class DicomImporter:
    def __init__(self, root):
        self.root = root
        self.root.title("DICOM Importer")
        self.root.geometry("800x600")
        
        # Variables
        self.current_file = None
        self.dicom_data = None
        
        # Create UI components
        self.create_menu()
        self.create_widgets()
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open DICOM File", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_widgets(self):
        """Create main UI widgets"""
        # Top frame with buttons
        top_frame = tk.Frame(self.root, bg="#f0f0f0", height=50)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        open_btn = tk.Button(top_frame, text="Open DICOM File", command=self.open_file, 
                            bg="#4CAF50", fg="white", padx=10, pady=5)
        open_btn.pack(side=tk.LEFT, padx=5)
        
        # Main content area with notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Image viewer tab
        self.image_frame = tk.Frame(self.notebook)
        self.notebook.add(self.image_frame, text="Image Viewer")
        
        self.canvas = tk.Canvas(self.image_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Metadata tab
        self.metadata_frame = tk.Frame(self.notebook)
        self.notebook.add(self.metadata_frame, text="Metadata")
        
        # Create text widget for metadata with scrollbar
        metadata_scroll = tk.Scrollbar(self.metadata_frame)
        metadata_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.metadata_text = tk.Text(self.metadata_frame, wrap=tk.WORD, 
                                     yscrollcommand=metadata_scroll.set)
        self.metadata_text.pack(fill=tk.BOTH, expand=True)
        metadata_scroll.config(command=self.metadata_text.yview)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, 
                                   anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def open_file(self):
        """Open and display a DICOM file"""
        filename = filedialog.askopenfilename(
            title="Select DICOM file",
            filetypes=[
                ("DICOM files", "*.dcm"),
                ("All files", "*.*")
            ]
        )
        
        if not filename:
            return
            
        try:
            # Read DICOM file
            self.dicom_data = pydicom.dcmread(filename)
            self.current_file = filename
            
            # Display image if available
            self.display_image()
            
            # Display metadata
            self.display_metadata()
            
            self.status_bar.config(text=f"Loaded: {os.path.basename(filename)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load DICOM file:\n{str(e)}")
            self.status_bar.config(text="Error loading file")
            
    def display_image(self):
        """Display the DICOM image"""
        if self.dicom_data is None:
            return
            
        try:
            # Get pixel array
            if not hasattr(self.dicom_data, 'pixel_array'):
                messagebox.showwarning("Warning", "This DICOM file does not contain image data")
                return
                
            pixel_array = self.dicom_data.pixel_array
            
            # Normalize to 8-bit
            pixel_array = pixel_array.astype(float)
            pixel_array = (pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min())
            pixel_array = (pixel_array * 255).astype(np.uint8)
            
            # Convert to PIL Image
            image = Image.fromarray(pixel_array)
            
            # Resize to fit canvas while maintaining aspect ratio
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                image.thumbnail((canvas_width - 10, canvas_height - 10), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.photo = ImageTk.PhotoImage(image)
            
            # Clear canvas and display image
            self.canvas.delete("all")
            self.canvas.create_image(
                canvas_width // 2 if canvas_width > 1 else 400,
                canvas_height // 2 if canvas_height > 1 else 300,
                anchor=tk.CENTER,
                image=self.photo
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display image:\n{str(e)}")
            
    def display_metadata(self):
        """Display DICOM metadata"""
        if self.dicom_data is None:
            return
            
        self.metadata_text.delete(1.0, tk.END)
        
        # Display file information
        if self.current_file:
            self.metadata_text.insert(tk.END, f"File: {os.path.basename(self.current_file)}\n")
            self.metadata_text.insert(tk.END, f"Path: {self.current_file}\n")
            self.metadata_text.insert(tk.END, "-" * 80 + "\n\n")
        
        # Display DICOM tags
        self.metadata_text.insert(tk.END, "DICOM Metadata:\n")
        self.metadata_text.insert(tk.END, "=" * 80 + "\n\n")
        
        for element in self.dicom_data:
            if element.VR != 'SQ':  # Skip sequences for simplicity
                try:
                    self.metadata_text.insert(tk.END, f"{element.tag} {element.name}: {element.value}\n")
                except:
                    self.metadata_text.insert(tk.END, f"{element.tag}: <unable to display>\n")
                    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About DICOM Importer",
            "DICOM Importer v1.0\n\n"
            "A simple GUI application for viewing DICOM medical image files.\n\n"
            "Built with Python, tkinter, and pydicom."
        )


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = DicomImporter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
