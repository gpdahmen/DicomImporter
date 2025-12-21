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
    /// Main class for exporting DICOM files to network folders or PACS
    /// </summary>
    public class DicomExporter
    {
        /// <summary>
        /// Export DICOM files to a local network folder
        /// </summary>
        /// <param name="sourceFiles">List of DICOM file paths to export</param>
        /// <param name="destinationPath">Destination network folder path</param>
        public async Task<int> ExportToFolderAsync(List<string> sourceFiles, string destinationPath)
        {
            if (!Directory.Exists(destinationPath))
            {
                Directory.CreateDirectory(destinationPath);
            }

            int exportedCount = 0;

            foreach (var sourceFile in sourceFiles)
            {
                try
                {
                    if (!File.Exists(sourceFile))
                    {
                        Console.WriteLine($"Source file not found: {sourceFile}");
                        continue;
                    }

                    var fileName = Path.GetFileName(sourceFile);
                    var destinationFile = Path.Combine(destinationPath, fileName);

                    File.Copy(sourceFile, destinationFile, overwrite: true);
                    exportedCount++;

                    Console.WriteLine($"Exported: {fileName}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error exporting {sourceFile}: {ex.Message}");
                }
            }

            Console.WriteLine($"Successfully exported {exportedCount} files to {destinationPath}");
            return exportedCount;
        }

        /// <summary>
        /// Export DICOM files to a PACS server using C-STORE
        /// </summary>
        /// <param name="sourceFiles">List of DICOM file paths to export</param>
        /// <param name="pacsHost">PACS server hostname or IP</param>
        /// <param name="pacsPort">PACS server port</param>
        /// <param name="pacsAeTitle">PACS Application Entity Title</param>
        /// <param name="clientAeTitle">Client Application Entity Title</param>
        public async Task<int> ExportToPacsAsync(
            List<string> sourceFiles,
            string pacsHost,
            int pacsPort,
            string pacsAeTitle,
            string clientAeTitle = "DICOM_IMPORTER")
        {
            int exportedCount = 0;

            try
            {
                Console.WriteLine($"Connecting to PACS server: {pacsHost}:{pacsPort} (AE: {pacsAeTitle})");

                foreach (var sourceFile in sourceFiles)
                {
                    try
                    {
                        if (!File.Exists(sourceFile))
                        {
                            Console.WriteLine($"Source file not found: {sourceFile}");
                            continue;
                        }

                        // Create DICOM client
                        var client = DicomClientFactory.Create(pacsHost, pacsPort, false, clientAeTitle, pacsAeTitle);

                        // Load DICOM file
                        var dicomFile = await DicomFile.OpenAsync(sourceFile);

                        // Create C-STORE request
                        var request = new DicomCStoreRequest(dicomFile);

                        request.OnResponseReceived += (req, response) =>
                        {
                            if (response.Status == DicomStatus.Success)
                            {
                                Console.WriteLine($"Successfully sent: {Path.GetFileName(sourceFile)}");
                                exportedCount++;
                            }
                            else
                            {
                                Console.WriteLine($"Failed to send {Path.GetFileName(sourceFile)}: {response.Status}");
                            }
                        };

                        // Add request to client
                        await client.AddRequestAsync(request);

                        // Send
                        await client.SendAsync();
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"Error sending {sourceFile} to PACS: {ex.Message}");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error connecting to PACS server: {ex.Message}");
                throw;
            }

            Console.WriteLine($"Successfully exported {exportedCount} files to PACS server");
            return exportedCount;
        }

        /// <summary>
        /// Test PACS connectivity
        /// </summary>
        public async Task<bool> TestPacsConnectionAsync(
            string pacsHost,
            int pacsPort,
            string pacsAeTitle,
            string clientAeTitle = "DICOM_IMPORTER")
        {
            try
            {
                Console.WriteLine($"Testing PACS connection to {pacsHost}:{pacsPort}...");

                var client = DicomClientFactory.Create(pacsHost, pacsPort, false, clientAeTitle, pacsAeTitle);

                // Create C-ECHO request
                var request = new DicomCEchoRequest();
                bool success = false;

                request.OnResponseReceived += (req, response) =>
                {
                    success = response.Status == DicomStatus.Success;
                };

                await client.AddRequestAsync(request);
                await client.SendAsync();

                Console.WriteLine(success ? "PACS connection successful" : "PACS connection failed");
                return success;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"PACS connection test failed: {ex.Message}");
                return false;
            }
        }
    }
}
