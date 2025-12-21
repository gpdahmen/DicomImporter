using FellowOakDicom;
using FellowOakDicom.Network;
using FellowOakDicom.Network.Client;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace DicomImporter
{
    /// <summary>
    /// Main class for importing DICOM files from external media
    /// </summary>
    public class DicomFileImporter
    {
        private readonly string _stagingDirectory;

        public DicomFileImporter(string stagingDirectory)
        {
            _stagingDirectory = stagingDirectory;
            if (!Directory.Exists(_stagingDirectory))
            {
                Directory.CreateDirectory(_stagingDirectory);
            }
        }

        /// <summary>
        /// Import DICOM files from a source directory (external media)
        /// </summary>
        /// <param name="sourcePath">Source directory path (CD/DVD/USB)</param>
        /// <returns>List of imported file paths</returns>
        public async Task<List<string>> ImportDicomFilesAsync(string sourcePath)
        {
            var importedFiles = new List<string>();

            if (!Directory.Exists(sourcePath))
            {
                throw new DirectoryNotFoundException($"Source directory not found: {sourcePath}");
            }

            Console.WriteLine($"Scanning for DICOM files in: {sourcePath}");

            // Recursively search for DICOM files
            var files = Directory.GetFiles(sourcePath, "*", SearchOption.AllDirectories);

            foreach (var file in files)
            {
                try
                {
                    // Try to open as DICOM file
                    var dicomFile = await DicomFile.OpenAsync(file);

                    // Generate unique filename
                    var dataset = dicomFile.Dataset;
                    var patientId = dataset.GetSingleValueOrDefault(DicomTag.PatientID, "UNKNOWN");
                    var studyInstanceUid = dataset.GetSingleValueOrDefault(DicomTag.StudyInstanceUID, Guid.NewGuid().ToString());
                    var sopInstanceUid = dataset.GetSingleValueOrDefault(DicomTag.SOPInstanceUID, Guid.NewGuid().ToString());

                    var fileName = $"{patientId}_{studyInstanceUid}_{sopInstanceUid}.dcm";
                    var destinationPath = Path.Combine(_stagingDirectory, fileName);

                    // Copy file to staging area
                    File.Copy(file, destinationPath, overwrite: true);
                    importedFiles.Add(destinationPath);

                    Console.WriteLine($"Imported: {Path.GetFileName(file)} -> {fileName}");
                }
                catch (DicomFileException)
                {
                    // Not a DICOM file, skip
                    continue;
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error importing {file}: {ex.Message}");
                }
            }

            Console.WriteLine($"Successfully imported {importedFiles.Count} DICOM files");
            return importedFiles;
        }

        /// <summary>
        /// Validate a DICOM file
        /// </summary>
        public static async Task<bool> ValidateDicomFileAsync(string filePath)
        {
            try
            {
                var dicomFile = await DicomFile.OpenAsync(filePath);
                return dicomFile != null;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Get DICOM file information
        /// </summary>
        public static async Task<Dictionary<string, string>> GetDicomInfoAsync(string filePath)
        {
            var info = new Dictionary<string, string>();

            try
            {
                var dicomFile = await DicomFile.OpenAsync(filePath);
                var dataset = dicomFile.Dataset;

                info["PatientID"] = dataset.GetSingleValueOrDefault(DicomTag.PatientID, "N/A");
                info["PatientName"] = dataset.GetSingleValueOrDefault(DicomTag.PatientName, "N/A");
                info["StudyDate"] = dataset.GetSingleValueOrDefault(DicomTag.StudyDate, "N/A");
                info["Modality"] = dataset.GetSingleValueOrDefault(DicomTag.Modality, "N/A");
                info["StudyDescription"] = dataset.GetSingleValueOrDefault(DicomTag.StudyDescription, "N/A");
                info["StudyInstanceUID"] = dataset.GetSingleValueOrDefault(DicomTag.StudyInstanceUID, "N/A");
            }
            catch (Exception ex)
            {
                info["Error"] = ex.Message;
            }

            return info;
        }
    }
}
