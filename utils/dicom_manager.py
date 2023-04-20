import os
import random
import string
import shutil
from datetime import datetime, timedelta
import pydicom.uid

from .pacs_util import modify_dicom_attributes


class DicomManager:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    @staticmethod
    def random_string(length):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    @staticmethod
    def random_date(start_date, end_date):
        delta = end_date - start_date
        random_days = random.randrange(delta.days)
        return start_date + timedelta(days=random_days)

    def generate_dicom_series(self, num_series):
        start_date = datetime(1950, 1, 1)
        end_date = datetime.today()

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        for i in range(num_series):

            new_patient_id = self.random_string(8)
            new_patient_name = self.random_string(5) + "^" + self.random_string(7)
            new_patient_birth_date = self.random_date(start_date, end_date).strftime("%Y%m%d")
            new_patient_sex = random.choice(["M", "F"])
            new_study_uid = pydicom.uid.generate_uid()
            new_series_uid = pydicom.uid.generate_uid()

            series_output_dir = os.path.join(self.output_dir, new_series_uid)
            os.makedirs(series_output_dir)
            modify_dicom_attributes(self.input_dir, series_output_dir, new_patient_id, new_patient_name,
                                    new_patient_birth_date, new_patient_sex, new_study_uid, new_series_uid)

    def delete_dicom_series(self):
        for directory in os.listdir(self.output_dir):
            dir_path = os.path.join(self.output_dir, directory)
            if os.path.isdir(dir_path):
                shutil.rmtree(dir_path)
                print(f"Deleted directory: {dir_path}")

    def get_series_directories(self):
        series_dirs = []
        for directory in os.listdir(self.output_dir):
            dir_path = os.path.join(self.output_dir, directory)
            if os.path.isdir(dir_path):
                series_dirs.append(dir_path)
        return series_dirs
