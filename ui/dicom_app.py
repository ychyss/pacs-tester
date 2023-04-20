import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout,QTextBrowser, QHBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from utils import DicomSender, DicomManager
from ui.send_thread import SendThread


class DicomApp(QtWidgets.QMainWindow):
    '''
    说明:
    输入请选择series文件夹,输出将产生多个series
    发送会同时发送所有的series到目标PACS
    '''
    def __init__(self):
        super().__init__()

        uic.loadUi('dicom_app.ui', self)
        # event
        self.generate_button.clicked.connect(self.generate_dicom)
        self.send_button.clicked.connect(self.send_dicom)
        self.delete_button.clicked.connect(self.delete_dicom)
        self.input_dir_btn.clicked.connect(self.select_input_directory)
        self.output_dir_btn.clicked.connect(self.select_output_directory)
        self.clear_log_button.clicked.connect(self.clear_log)
        # self.delete_pacs_button.clicked.connect(self.delete_pacs_studies)
        # 存储值
        self.input_directory = os.getcwd()
        self.output_directory = None
        # 默认值
        self.input_dir_edit.setText(self.input_directory)

    def log_message(self, msg, msg_type='info'):
        color_map = {
            'success': 'green',
            'info': 'black',
            'warning': 'orange',
            'error': 'red'
        }

        color = color_map.get(msg_type, 'black')
        self.log_viewer.append(f'<span style="color:{color}">{msg}</span>')

    def clear_log(self):
        self.log_viewer.setText('')

    def append_to_log(self, stdout, stderr, finish_time):
        if stdout:
            self.log_message(stdout)
        if stderr:
            self.log_message(stderr, msg_type="error")
        self.log_message(f"time used: {finish_time}s")
        self.log_message("===============================")

    def select_input_directory(self):
        self.input_directory = QFileDialog.getExistingDirectory(self, 'Select Input Directory', directory=self.input_directory)
        self.input_dir_edit.setText(self.input_directory)
        self.log_message(f'Selected Input Directory: {self.input_directory}')

    def select_output_directory(self):
        self.output_directory = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        self.output_dir_edit.setText(self.output_directory)
        self.log_message(f'Selected Output Directory: {self.output_directory}')

    def on_send_finished(self, finish_time):
        self.log_message(f"DICOM series sending finished. time {finish_time}s", msg_type="success")

    def send_dicom(self):
        if self.output_directory is None:
            self.log_message('Please select an output directory.', 'error')
            return
        # Check if the output directory has any files
        manager = DicomManager(input_dir=self.input_directory, output_dir=self.output_directory)
        series_dirs = manager.get_series_directories()  # Fix the method call here
        if len(series_dirs) < 1:
            self.log_viewer.append("No series found in the output directory.")
            return

        gateway_ae = self.gateway_ae_edit.text()
        gateway_host = self.gateway_host_edit.text()
        gateway_port = int(self.gateway_port_edit.text())
        dcm4che_path = self.dcm4che_path_edit.text()

        sender = DicomSender(gateway_ae=gateway_ae, gateway_host=gateway_host, gateway_port=gateway_port, dcm4che_path=dcm4che_path)
        max_workers = self.worker_num.value()
        self.log_message("Sending DICOM series...")

        self.send_thread = SendThread(sender, series_dirs, max_workers)
        self.send_thread.log_signal.connect(self.append_to_log)
        self.send_thread.finished_signal.connect(self.on_send_finished)
        self.send_thread.start()

        # print("worker=", max_workers)
        # sender.send_multiple_dicom_series(series_dirs, callback=append_to_log, max_workers=max_workers)
        #
        # self.log_message("Sending DICOM Finished.")

    # def delete_pacs_studies(self):
    #
    #     gateway_ae = self.gateway_ae_edit.text()
    #     gateway_host = self.gateway_host_edit.text()
    #     gateway_port = int(self.gateway_port_edit.text())
    #     dcm4che_path = self.dcm4che_path_edit.text()
    #
    #     sender = DicomSender(gateway_ae=gateway_ae, gateway_host=gateway_host, gateway_port=gateway_port,
    #                          dcm4che_path=dcm4che_path)
    #
    #     def print_log(stdout, stderr):
    #         if stdout:
    #             self.log_message(stdout)
    #         if stderr:
    #             self.log_message(stderr, msg_type="error")
    #
    #     sender.delete_all_studies(print_log)

    def generate_dicom(self):
        if self.input_directory is None:
            self.log_message('Please select an input directory.', 'error')
            return
        if self.output_directory is None:
            self.log_message('Please select an output directory.', 'error')
            return
        self.log_message('DICOM files generating...')
        series_count = self.series_count_spinbox.value()
        manager = DicomManager(input_dir=self.input_directory, output_dir=self.output_directory)
        manager.generate_dicom_series(series_count)
        self.log_message(f'DICOM files generated in: {self.output_directory}', msg_type="success")

    def delete_dicom(self):
        if self.output_directory is None:
            self.log_message('Please select an output directory.', 'error')
            return

        manager = DicomManager(input_dir=self.input_directory, output_dir=self.output_directory)
        manager.delete_dicom_series()
        self.log_message(f'Deleted generated DICOM files in: {self.output_directory}', msg_type="success")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DicomApp()
    window.show()
    sys.exit(app.exec_())

