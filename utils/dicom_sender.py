import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import requests


class SendResult:
    def __init__(self, series_dir, success, duration, error=None):
        self.series_dir = series_dir
        self.success = success
        self.duration = duration
        self.error = error

    def __str__(self):
        if self.success:
            return f'Successfully sent series {self.series_dir} in {self.duration:.2f} seconds'
        else:
            return f'Error sending series {self.series_dir} in {self.duration:.2f} seconds: {self.error}'


class DicomSender:
    """
    该测试用于向网关并发发送多个存储，以确保网关能够正确导出到其他存储库
    """

    def __init__(self, gateway_ae, gateway_host, gateway_port, dcm4che_path='/home/hys/apps/dcm4che-5.26.0'):
        self.gateway_ae = gateway_ae
        self.gateway_host = gateway_host
        self.gateway_port = gateway_port
        self.dcm4che_path = dcm4che_path

    def send_directory(self, dicom_directory):
        storescu_path = os.path.join(self.dcm4che_path, 'bin', 'storescu')
        cmd = [storescu_path, '-c', f'{self.gateway_ae}@{self.gateway_host}:{self.gateway_port}', dicom_directory]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        return stdout.decode('utf-8'), stderr.decode('utf-8')

    def send_dicom_series(self, series_dir):
        storescu_path = os.path.join(self.dcm4che_path, 'bin', 'storescu')
        start_time = time.perf_counter()
        success = True
        error = None

        for root, _, files in os.walk(series_dir):
          for dicom_file in files:
              if dicom_file.lower().endswith('.dcm'):  # 只处理 .dcm 文件
                  dicom_path = os.path.join(root, dicom_file)

                  # 构建 storescu 命令
                  cmd = [
                      storescu_path,
                      '-c', f'{self.gateway_ae}@{self.gateway_host}:{self.gateway_port}',
                      dicom_path
                  ]

                  try:
                      result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                      print(f'Successfully sent {dicom_path}:\n{result.stdout}')
                  except subprocess.CalledProcessError as e:
                      success = False
                      error = e
                      print(f'Error sending {dicom_path}:\n{e.output}')
                      break

          if not success:
              break

        duration = time.perf_counter() - start_time
        return SendResult(series_dir, success, duration, error)

    def send_multiple_dicom_series(self, series_dirs, callback=None, max_workers=4):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.send_directory, series_dir) for series_dir in series_dirs]

            def process_future(future):
                stdout, stderr = future.result()  # Extract stdout and stderr
                if callback:
                    callback(stdout, stderr)

            for future in as_completed(futures):
                process_future(future)

    def query_all_studies(self):
        findscu_path = os.path.join(self.dcm4che_path, 'bin', 'findscu')
        findscu_command = [findscu_path, '-c', f'{self.gateway_ae}@{self.gateway_host}:{self.gateway_port}', '-L', 'STUDY', '-m', 'StudyInstanceUID=*']
        output = subprocess.check_output(" ".join(findscu_command), shell=True, text=True)

        study_instance_uids = []
        for line in output.splitlines():
            match = re.search(r'\(0020,000D\) UI \[([0-9a-zA-Z\.-]+)', line)
            if match:
                study_instance_uid = match.group(1)
                study_instance_uids.append(study_instance_uid)

        return study_instance_uids

    def delete_study(self, study_instance_uid):
        # movescu_path = os.path.join(self.dcm4che_path, 'bin', 'movescu')
        # movescu_command = [movescu_path, '-c', f'{self.gateway_ae}@{self.gateway_host}:{self.gateway_port}', '-m', f'StudyInstanceUID={study_instance_uid}', '--dest', 'FAKE_AE']
        # process = subprocess.Popen(movescu_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # stdout, stderr = process.communicate()

        # http://test-ng:8080/dcm4chee-arc/aets/DCM_GATEWAY/rs/studies/1.2.826.0.1.3680043.8.498.866432210749273532730074963361952162?retainObj=false
        url = f'https://192.168.1.200:32002/dcm4chee-arc/aets/DCM_GATEWAY/rs/studies/{study_instance_uid}?retainObj=false'
        print(url)
        response = requests.delete(url, verify=False)

        if response.status_code == 204:
            return "Study with UID {} deleted successfully.".format(study_instance_uid), ""
        else:
            return None, "Error deleting study with UID {}. Status code: {}".format(study_instance_uid, response.status_code)

    def delete_all_studies(self, callback):
        study_instance_uids = self.query_all_studies()
        # print("uids:", study_instance_uids)
        for study_instance_uid in study_instance_uids:
            stdout, stderr = self.delete_study(study_instance_uid)
            if callback:
                callback(stdout, stderr)
