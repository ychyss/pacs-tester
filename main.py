import sys
import argparse
from PyQt5.QtWidgets import QApplication
from ui.dicom_app import DicomApp
from utils.dicom_manager import DicomManager
from utils.dicom_sender import DicomSender
import time

def main():
    parser = argparse.ArgumentParser(description="PACS Tester - A tool to generate, send, and delete DICOM series for testing PACS systems")
    parser.add_argument('--gui', action='store_true', help="Run the application in GUI mode")
    parser.add_argument('--generate', action='store_true', help="Generate DICOM series (command-line mode)")
    parser.add_argument('--send', action='store_true', help="Send generated DICOM series to PACS (command-line mode)")
    parser.add_argument('--delete', action='store_true', help="Delete generated DICOM series (command-line mode)")
    parser.add_argument('--input-dir', type=str, help="Input directory for generating DICOM series (required for command-line mode)")
    parser.add_argument('--output-dir', type=str, help="Output directory for generated DICOM series (required for command-line mode)")
    parser.add_argument('--series-count', type=int, help="Number of series to generate (required for --generate mode)")
    parser.add_argument('--gateway-ae', type=str, help="Gateway AE (required for --send mode)")
    parser.add_argument('--gateway-host', type=str, help="Gateway Host (required for --send mode)")
    parser.add_argument('--gateway-port', type=int, help="Gateway Port (required for --send mode)")
    parser.add_argument('--dcm4che-path', type=str, help="Dcm4che path (required for --send mode)")
    parser.add_argument('--max-workers', type=int, help="Number of workers (required for --send mode)")

    args = parser.parse_args()
    # 如果没参数就直接启动GUI
    if args.gui or len(sys.argv) == 1:
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
            if not args.series_count:
                print("Series count must be specified for --generate mode.")
                sys.exit(1)

            manager.generate_dicom_series(args.series_count)
            print(f"DICOM files generated in: {args.output_dir}")

        if args.send:
            if not args.gateway_ae or not args.gateway_host or not args.gateway_port or not args.dcm4che_path or not args.max_workers:
                print("Gateway AE, Gateway Host, Gateway Port, Dcm4che path, and Max workers must be specified for --send mode.")
                sys.exit(1)
            start_time = time.time()
            sender = DicomSender(gateway_ae=args.gateway_ae, gateway_host=args.gateway_host, gateway_port=args.gateway_port, dcm4che_path=args.dcm4che_path)
            series_dirs = manager.get_series_directories()
            sender.send_multiple_dicom_series(series_dirs, max_workers=args.max_workers)
            end_time = time.time()
            print("Sending DICOM series finished." + str(end_time - start_time))

        if args.delete:
            manager.delete_dicom_series()
            print(f"Deleted generated DICOM files in: {args.output_dir}")


if __name__ == "__main__":
    main()
