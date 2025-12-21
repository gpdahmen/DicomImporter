using DicomImporter;
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;

namespace DicomImporter
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("=== DICOM Importer/Exporter Application ===");
            Console.WriteLine();

            if (args.Length == 0)
            {
                ShowHelp();
                return;
            }

            var command = args[0].ToLower();

            try
            {
                switch (command)
                {
                    case "import":
                        await HandleImportCommand(args);
                        break;

                    case "export-folder":
                        await HandleExportFolderCommand(args);
                        break;

                    case "export-pacs":
                        await HandleExportPacsCommand(args);
                        break;

                    case "test-pacs":
                        await HandleTestPacsCommand(args);
                        break;

                    case "info":
                        await HandleInfoCommand(args);
                        break;

                    case "help":
                    case "--help":
                    case "-h":
                        ShowHelp();
                        break;

                    default:
                        Console.WriteLine($"Unknown command: {command}");
                        Console.WriteLine();
                        ShowHelp();
                        break;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
                Environment.Exit(1);
            }
        }

        static async Task HandleImportCommand(string[] args)
        {
            if (args.Length < 3)
            {
                Console.WriteLine("Usage: DicomImporter import <source-path> <staging-path>");
                Console.WriteLine("  source-path: Path to external media (CD/DVD/USB)");
                Console.WriteLine("  staging-path: Path to staging directory");
                return;
            }

            var sourcePath = args[1];
            var stagingPath = args[2];

            var importer = new DicomFileImporter(stagingPath);
            var importedFiles = await importer.ImportDicomFilesAsync(sourcePath);

            Console.WriteLine();
            Console.WriteLine($"Import complete. {importedFiles.Count} files imported to {stagingPath}");
        }

        static async Task HandleExportFolderCommand(string[] args)
        {
            if (args.Length < 3)
            {
                Console.WriteLine("Usage: DicomImporter export-folder <source-path> <destination-path>");
                Console.WriteLine("  source-path: Path to directory containing DICOM files");
                Console.WriteLine("  destination-path: Path to network folder");
                return;
            }

            var sourcePath = args[1];
            var destinationPath = args[2];

            if (!Directory.Exists(sourcePath))
            {
                Console.WriteLine($"Source directory not found: {sourcePath}");
                return;
            }

            var files = new List<string>(Directory.GetFiles(sourcePath, "*.dcm", SearchOption.AllDirectories));
            
            if (files.Count == 0)
            {
                Console.WriteLine("No DICOM files found in source directory");
                return;
            }

            var exporter = new DicomExporter();
            var exportedCount = await exporter.ExportToFolderAsync(files, destinationPath);

            Console.WriteLine();
            Console.WriteLine($"Export complete. {exportedCount} files exported to {destinationPath}");
        }

        static async Task HandleExportPacsCommand(string[] args)
        {
            if (args.Length < 5)
            {
                Console.WriteLine("Usage: DicomImporter export-pacs <source-path> <pacs-host> <pacs-port> <pacs-ae-title> [client-ae-title]");
                Console.WriteLine("  source-path: Path to directory containing DICOM files");
                Console.WriteLine("  pacs-host: PACS server hostname or IP address");
                Console.WriteLine("  pacs-port: PACS server port");
                Console.WriteLine("  pacs-ae-title: PACS Application Entity Title");
                Console.WriteLine("  client-ae-title: Client Application Entity Title (optional, default: DICOM_IMPORTER)");
                return;
            }

            var sourcePath = args[1];
            var pacsHost = args[2];
            
            if (!int.TryParse(args[3], out var pacsPort))
            {
                Console.WriteLine($"Invalid port number: {args[3]}");
                return;
            }
            
            var pacsAeTitle = args[4];
            var clientAeTitle = args.Length > 5 ? args[5] : "DICOM_IMPORTER";

            if (!Directory.Exists(sourcePath))
            {
                Console.WriteLine($"Source directory not found: {sourcePath}");
                return;
            }

            var files = new List<string>(Directory.GetFiles(sourcePath, "*.dcm", SearchOption.AllDirectories));
            
            if (files.Count == 0)
            {
                Console.WriteLine("No DICOM files found in source directory");
                return;
            }

            var exporter = new DicomExporter();
            var exportedCount = await exporter.ExportToPacsAsync(files, pacsHost, pacsPort, pacsAeTitle, clientAeTitle);

            Console.WriteLine();
            Console.WriteLine($"Export complete. {exportedCount} files exported to PACS server");
        }

        static async Task HandleTestPacsCommand(string[] args)
        {
            if (args.Length < 4)
            {
                Console.WriteLine("Usage: DicomImporter test-pacs <pacs-host> <pacs-port> <pacs-ae-title> [client-ae-title]");
                Console.WriteLine("  pacs-host: PACS server hostname or IP address");
                Console.WriteLine("  pacs-port: PACS server port");
                Console.WriteLine("  pacs-ae-title: PACS Application Entity Title");
                Console.WriteLine("  client-ae-title: Client Application Entity Title (optional, default: DICOM_IMPORTER)");
                return;
            }

            var pacsHost = args[1];
            
            if (!int.TryParse(args[2], out var pacsPort))
            {
                Console.WriteLine($"Invalid port number: {args[2]}");
                return;
            }
            
            var pacsAeTitle = args[3];
            var clientAeTitle = args.Length > 4 ? args[4] : "DICOM_IMPORTER";

            var exporter = new DicomExporter();
            var success = await exporter.TestPacsConnectionAsync(pacsHost, pacsPort, pacsAeTitle, clientAeTitle);

            Environment.Exit(success ? 0 : 1);
        }

        static async Task HandleInfoCommand(string[] args)
        {
            if (args.Length < 2)
            {
                Console.WriteLine("Usage: DicomImporter info <dicom-file-path>");
                Console.WriteLine("  dicom-file-path: Path to DICOM file");
                return;
            }

            var filePath = args[1];

            if (!File.Exists(filePath))
            {
                Console.WriteLine($"File not found: {filePath}");
                return;
            }

            var info = await DicomFileImporter.GetDicomInfoAsync(filePath);

            Console.WriteLine("DICOM File Information:");
            Console.WriteLine("----------------------");
            foreach (var kvp in info)
            {
                Console.WriteLine($"{kvp.Key}: {kvp.Value}");
            }
        }

        static void ShowHelp()
        {
            Console.WriteLine("DICOM Importer/Exporter - Facilitates import and export of DICOM files");
            Console.WriteLine();
            Console.WriteLine("Usage: DicomImporter <command> [options]");
            Console.WriteLine();
            Console.WriteLine("Commands:");
            Console.WriteLine("  import <source-path> <staging-path>");
            Console.WriteLine("      Import DICOM files from external media (CD/DVD/USB) to staging area");
            Console.WriteLine();
            Console.WriteLine("  export-folder <source-path> <destination-path>");
            Console.WriteLine("      Export DICOM files to a local network folder");
            Console.WriteLine();
            Console.WriteLine("  export-pacs <source-path> <pacs-host> <pacs-port> <pacs-ae-title> [client-ae-title]");
            Console.WriteLine("      Export DICOM files to a PACS server using C-STORE");
            Console.WriteLine();
            Console.WriteLine("  test-pacs <pacs-host> <pacs-port> <pacs-ae-title> [client-ae-title]");
            Console.WriteLine("      Test connectivity to a PACS server using C-ECHO");
            Console.WriteLine();
            Console.WriteLine("  info <dicom-file-path>");
            Console.WriteLine("      Display information about a DICOM file");
            Console.WriteLine();
            Console.WriteLine("  help");
            Console.WriteLine("      Display this help message");
            Console.WriteLine();
            Console.WriteLine("Examples:");
            Console.WriteLine("  DicomImporter import /media/cdrom /tmp/dicom-staging");
            Console.WriteLine("  DicomImporter export-folder /tmp/dicom-staging /mnt/network/dicom");
            Console.WriteLine("  DicomImporter export-pacs /tmp/dicom-staging 192.168.1.100 104 PACS_SERVER");
            Console.WriteLine("  DicomImporter test-pacs 192.168.1.100 104 PACS_SERVER");
            Console.WriteLine("  DicomImporter info /tmp/dicom-staging/sample.dcm");
        }
    }
}
