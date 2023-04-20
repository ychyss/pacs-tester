from PyQt5.QtCore import QThread, pyqtSignal
import time


class SendThread(QThread):
    """
    发送线程, 子线程发送, 主线程用于显示UI
    """
    log_signal = pyqtSignal(str, str, float)
    finished_signal = pyqtSignal(float)

    def __init__(self, dicom_sender, series_dirs, max_workers):
        super(SendThread, self).__init__()
        self.dicom_sender = dicom_sender
        self.series_dirs = series_dirs
        self.max_workers = max_workers
        self.send_count = 0

    def run(self):
        self.start_time = time.time()
        self.checkpoint_time = time.time()
        self.dicom_sender.send_multiple_dicom_series(self.series_dirs,
                                                     callback=self.append_to_log,
                                                     max_workers=self.max_workers)

    def append_to_log(self, stdout, stderr):
        self.send_count += 1
        consumed = time.time() - self.checkpoint_time
        self.checkpoint_time = time.time()
        self.log_signal.emit(stdout, stderr, consumed)
        if self.send_count == len(self.series_dirs):
            self.finished_signal.emit(time.time() - self.start_time)
