import sys
import argparse
from PyQt5.QtWidgets import QApplication
from ui.dicom_app import DicomApp
from utils.dicom_manager import DicomManager
from utils.dicom_sender import DicomSender


def main():
    parser = argparse.ArgumentParser(description="PACS Tester - A tool to generate, send, and delete DICOM series for testing PACS systems")
    parser.add_argument('--gui', action='store_true', help="Run the application in GUI mode")
    parser.add_argument('--generate', action='store_true', help="Generate DICOM series (command-line mode)")
    parser.add_argument('--send', action='store_true', help="Send generated DICOM series to PACS (command-line mode)")
    parser.add_argument('--delete', action='store_true', help="Delete generated DICOM series (command-line mode)")
    parser.add_argument('--input-dir', type=str, help="Input directory for generating DICOM series (required for command-line mode)")
    parser.add_argument('--output-dir', type=str, help="Output directory for generated DICOM series (required for command-line mode)")

    args = parser.parse_args()

    if args.gui:
        app = QApplication(sys.argv)
        window = DicomApp()
        window.show()
        sys.exit(app.exec_())
    else:
        if not args.input_dir or not args.output_dir:
            print("Input and output directories must be specified for command-line usage.")
            sys.exit(1)

        manager = DicomManager(input_dir=args.input_dir, output_dir=args.output_dir)

        if args.generate:
            series_count = int(input("Enter the number of series to generate: "))
            manager.generate_dicom_series(series_count)
            print(f"DICOM files generated in: {args.output_dir}")

        if args.send:
            gateway_ae = input("Enter Gateway AE: ")
            gateway_host = input("Enter Gateway Host: ")
            gateway_port = int(input("Enter Gateway Port: "))
            dcm4che_path = input("Enter dcm4che path: ")
            max_workers = int(input("Enter the number of workers: "))

            sender = DicomSender(gateway_ae=gateway_ae, gateway_host=gateway_host, gateway_port=gateway_port, dcm4che_path=dcm4che_path)
            series_dirs = manager.get_series_directories()
            sender.send_multiple_dicom_series(series_dirs, max_workers=max_workers)
            print("Sending DICOM series finished.")

        if args.delete:
            manager.delete_dicom_series()
            print(f"Deleted generated DICOM files in: {args.output_dir}")


if __name__ == "__main__":
    main()
