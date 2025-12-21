"""
DICOM Import/Export Application - Main GUI

This application facilitates the import of DICOM files from external media
and their export to either a local network folder or a PACS server.
"""

import os
import threading
from tkinter import filedialog
import customtkinter as ctk

from dicom_engine import DicomEngine


class DicomApp:
    """
    Main GUI application for DICOM import/export operations.
    """

    def __init__(self):
        """Initialize the DICOM application."""
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("DICOM Import/Export Application")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)

        # Initialize engine
        self.engine = DicomEngine(log_callback=self.log_message)

        # State variables
        self.source_dir = ""
        self.dest_dir = ""
        self.is_running = False

        # Build GUI
        self._build_gui()

    def _build_gui(self):
        """Build the GUI components."""
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="DICOM Import/Export Application",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Source directory section
        source_frame = ctk.CTkFrame(main_frame)
        source_frame.pack(fill="x", pady=10)

        source_label = ctk.CTkLabel(
            source_frame,
            text="Source Directory:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        source_label.pack(anchor="w", padx=10, pady=(10, 5))

        source_path_frame = ctk.CTkFrame(source_frame)
        source_path_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.source_entry = ctk.CTkEntry(
            source_path_frame,
            placeholder_text="Select source directory (e.g., D:\ for CD/DVD)"
        )
        self.source_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        source_browse_btn = ctk.CTkButton(
            source_path_frame,
            text="Browse Source",
            command=self.browse_source,
            width=150
        )
        source_browse_btn.pack(side="right")

        # Destination type section
        dest_type_frame = ctk.CTkFrame(main_frame)
        dest_type_frame.pack(fill="x", pady=10)

        dest_type_label = ctk.CTkLabel(
            dest_type_frame,
            text="Destination Type:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        dest_type_label.pack(anchor="w", padx=10, pady=(10, 5))

        # Radio buttons for destination type
        self.dest_type_var = ctk.StringVar(value="folder")

        radio_frame = ctk.CTkFrame(dest_type_frame)
        radio_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.folder_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Folder",
            variable=self.dest_type_var,
            value="folder",
            command=self.toggle_destination_type
        )
        self.folder_radio.pack(side="left", padx=10)

        self.pacs_radio = ctk.CTkRadioButton(
            radio_frame,
            text="PACS Server",
            variable=self.dest_type_var,
            value="pacs",
            command=self.toggle_destination_type
        )
        self.pacs_radio.pack(side="left", padx=10)

        # Folder destination section
        self.folder_frame = ctk.CTkFrame(main_frame)
        self.folder_frame.pack(fill="x", pady=10)

        folder_label = ctk.CTkLabel(
            self.folder_frame,
            text="Destination Folder:",
            font=ctk.CTkFont(size=14)
        )
        folder_label.pack(anchor="w", padx=10, pady=(10, 5))

        folder_path_frame = ctk.CTkFrame(self.folder_frame)
        folder_path_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.folder_entry = ctk.CTkEntry(
            folder_path_frame,
            placeholder_text="Select destination folder"
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        folder_browse_btn = ctk.CTkButton(
            folder_path_frame,
            text="Browse Folder",
            command=self.browse_folder,
            width=150
        )
        folder_browse_btn.pack(side="right")

        # PACS destination section
        self.pacs_frame = ctk.CTkFrame(main_frame)

        pacs_label = ctk.CTkLabel(
            self.pacs_frame,
            text="PACS Server Configuration:",
            font=ctk.CTkFont(size=14)
        )
        pacs_label.pack(anchor="w", padx=10, pady=(10, 5))

        # PACS fields
        pacs_fields_frame = ctk.CTkFrame(self.pacs_frame)
        pacs_fields_frame.pack(fill="x", padx=10, pady=(0, 10))

        # AE Title
        ae_label = ctk.CTkLabel(pacs_fields_frame, text="AE Title (This App):", width=150)
        ae_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ae_title_entry = ctk.CTkEntry(pacs_fields_frame)
        self.ae_title_entry.insert(0, "DICOM_IMPORTER")
        self.ae_title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Called AE Title
        called_ae_label = ctk.CTkLabel(pacs_fields_frame, text="Called AE Title:", width=150)
        called_ae_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.called_ae_entry = ctk.CTkEntry(pacs_fields_frame)
        self.called_ae_entry.insert(0, "ANY-SCP")
        self.called_ae_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # IP Address
        ip_label = ctk.CTkLabel(pacs_fields_frame, text="PACS IP Address:", width=150)
        ip_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ip_entry = ctk.CTkEntry(pacs_fields_frame)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Port
        port_label = ctk.CTkLabel(pacs_fields_frame, text="PACS Port:", width=150)
        port_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.port_entry = ctk.CTkEntry(pacs_fields_frame)
        self.port_entry.insert(0, "11112")
        self.port_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        pacs_fields_frame.columnconfigure(1, weight=1)

        # Progress section
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", pady=10)

        progress_label = ctk.CTkLabel(
            progress_frame,
            text="Progress:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        progress_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=(0, 5))
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(progress_frame, text="Ready")
        self.progress_label.pack(anchor="w", padx=10, pady=(0, 10))

        # Log section
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True, pady=10)

        log_label = ctk.CTkLabel(
            log_frame,
            text="Activity Log:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        log_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.log_text = ctk.CTkTextbox(log_frame, height=150)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Control buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=10)

        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start Import/Export",
            command=self.start_import_export,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.start_button.pack(side="left", expand=True, fill="x", padx=5)

        self.stop_button = ctk.CTkButton(
            button_frame,
            text="Clear Log",
            command=self.clear_log,
            height=40,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.stop_button.pack(side="right", padx=5)

        # Initialize visibility
        self.toggle_destination_type()

    def toggle_destination_type(self):
        """Toggle visibility of folder/PACS configuration sections."""
        if self.dest_type_var.get() == "folder":
            self.folder_frame.pack(fill="x", pady=10, after=self.dest_type_var.master.master)
            self.pacs_frame.pack_forget()
        else:
            self.pacs_frame.pack(fill="x", pady=10, after=self.dest_type_var.master.master)
            self.folder_frame.pack_forget()

    def browse_source(self):
        """Open file dialog to select source directory."""
        directory = filedialog.askdirectory(title="Select Source Directory")
        if directory:
            self.source_dir = directory
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, directory)
            self.log_message(f"Source directory selected: {directory}")

    def browse_folder(self):
        """Open file dialog to select destination folder."""
        directory = filedialog.askdirectory(title="Select Destination Folder")
        if directory:
            self.dest_dir = directory
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, directory)
            self.log_message(f"Destination folder selected: {directory}")

    def log_message(self, message: str):
        """
        Add a message to the log window.

        Args:
            message: Message to log.
        """
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    def clear_log(self):
        """Clear the log window."""
        self.log_text.delete("1.0", "end")

    def update_progress(self, current: int, total: int):
        """
        Update the progress bar.

        Args:
            current: Current progress value.
            total: Total progress value.
        """
        if total > 0:
            progress = current / total
            self.progress_bar.set(progress)
            self.progress_label.configure(text=f"Progress: {current}/{total} ({progress*100:.1f}%)")

    def start_import_export(self):
        """Start the import/export process in a background thread."""
        if self.is_running:
            self.log_message("Operation already in progress")
            return

        # Validate inputs
        source = self.source_entry.get().strip()
        if not source or not os.path.exists(source):
            self.log_message("ERROR: Please select a valid source directory")
            return

        dest_type = self.dest_type_var.get()

        if dest_type == "folder":
            dest_folder = self.folder_entry.get().strip()
            if not dest_folder:
                self.log_message("ERROR: Please select a destination folder")
                return
        else:  # PACS
            ae_title = self.ae_title_entry.get().strip()
            called_ae = self.called_ae_entry.get().strip()
            pacs_ip = self.ip_entry.get().strip()
            pacs_port = self.port_entry.get().strip()

            if not all([ae_title, called_ae, pacs_ip, pacs_port]):
                self.log_message("ERROR: Please fill in all PACS configuration fields")
                return

            try:
                pacs_port = int(pacs_port)
            except ValueError:
                self.log_message("ERROR: PACS port must be a valid number")
                return

        # Disable start button during operation
        self.is_running = True
        self.start_button.configure(state="disabled", text="Operation in Progress...")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Starting...")

        # Run in background thread
        thread = threading.Thread(
            target=self._run_import_export,
            args=(source, dest_type),
            daemon=True
        )
        thread.start()

    def _run_import_export(self, source: str, dest_type: str):
        """
        Execute the import/export operation.

        Args:
            source: Source directory path.
            dest_type: Type of destination ('folder' or 'pacs').
        """
        try:
            self.log_message("="*60)
            self.log_message("Starting DICOM Import/Export Operation")
            self.log_message("="*60)

            # Step 1: Cache files
            self.log_message("\nPhase 1: Caching DICOM files from source...")
            cached, total = self.engine.cache_files(
                source,
                progress_callback=self.update_progress
            )

            if cached == 0:
                self.log_message("\nNo DICOM files found in source directory")
                return

            # Step 2: Export to destination
            self.log_message(f"\nPhase 2: Exporting to {dest_type}...")
            self.progress_bar.set(0)

            if dest_type == "folder":
                dest_folder = self.folder_entry.get().strip()
                exported = self.engine.send_to_folder(
                    dest_folder,
                    progress_callback=self.update_progress
                )
                self.log_message(f"\nExport complete: {exported} files copied to {dest_folder}")
            else:  # PACS
                ae_title = self.ae_title_entry.get().strip()
                called_ae = self.called_ae_entry.get().strip()
                pacs_ip = self.ip_entry.get().strip()
                pacs_port = int(self.port_entry.get().strip())

                exported = self.engine.send_to_pacs(
                    ae_title=ae_title,
                    pacs_ip=pacs_ip,
                    pacs_port=pacs_port,
                    called_ae_title=called_ae,
                    progress_callback=self.update_progress
                )
                self.log_message(f"\nPACS export complete: {exported} files sent to {pacs_ip}:{pacs_port}")

            # Step 3: Cleanup
            self.log_message("\nPhase 3: Cleaning up temporary cache...")
            self.engine.cleanup()

            self.log_message("\n" + "="*60)
            self.log_message("Operation completed successfully!")
            self.log_message("="*60)

        except Exception as e:
            self.log_message(f"\nERROR: {str(e)}")
            import traceback
            self.log_message(traceback.format_exc())

        finally:
            # Re-enable start button
            self.is_running = False
            self.start_button.configure(state="normal", text="Start Import/Export")
            self.progress_label.configure(text="Operation complete")

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


def main():
    """Main entry point for the application."""
    app = DicomApp()
    app.run()


if __name__ == "__main__":
    main()
