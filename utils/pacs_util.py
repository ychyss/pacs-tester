import os
import pydicom
import pydicom.uid
import datetime
import platform

def is_linux():
    return platform.system() == "Linux"


def is_windows():
    return platform.system() == "Windows"


def modify_dicom_attributes(input_dir, output_dir, new_patient_id, new_patient_name, new_patient_birth_date,
                            new_patient_sex, new_study_uid, new_series_uid):
    """
    修改一个序列的信息
    :param input_dir:
    :param output_dir:
    :param new_patient_id:
    :param new_patient_name:
    :param new_patient_birth_date:
    :param new_patient_sex:
    :param new_study_uid:
    :param new_series_uid:
    :return:
    """

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".dcm"):
                input_file = os.path.join(root, file)
                ds = pydicom.dcmread(input_file)

                ds.PatientID = new_patient_id
                ds.PatientName = new_patient_name
                ds.PatientBirthDate = new_patient_birth_date
                ds.PatientSex = new_patient_sex
                ds.StudyInstanceUID = new_study_uid
                ds.SeriesInstanceUID = new_series_uid
                ds.SOPInstanceUID = pydicom.uid.generate_uid()
                ds.StudyDescription = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")

                output_file = os.path.join(output_dir, file)
                ds.save_as(output_file)


if __name__ == '__main__':
    pass
    # 示例：批量修改指定目录中的 DICOM 文件的 PatientID、PatientName、PatientBirthDate 和 PatientSex，并将修改后的文件保存到新目录
    series_dir = '../source_data/Ankle'
    new_series_dir = '../test_data/hys_ankle'
    if not os.path.exists(new_series_dir):
        os.mkdir(new_series_dir)
    new_patient_id = 'GMABC125135'
    new_patient_name = 'Yangsheng Hu'
    new_patient_birthdate = '20100401'  # 使用 YYYYMMDD 格式
    new_patient_sex = 'M'  # 使用 'M'（男性）或 'F'（女性）
    new_study_uid = pydicom.uid.generate_uid()
    new_series_uid = pydicom.uid.generate_uid()

    modify_dicom_attributes(series_dir, new_series_dir,
                            new_patient_id, new_patient_name, new_patient_birthdate, new_patient_sex,
                            new_study_uid, new_series_uid)
    # 发送多个series到pacs
    # dcm4che_path = '/apps/dcm4che-5.26.0'
    # series_dirs = ['path/to/your/series1', 'path/to/your/series2', 'path/to/your/series3']
    # gateway_pacs_aet = 'GATEWAY_PACS_AET'  # 网关 PACS 系统的 AETitle
    # gateway_pacs_ip = '192.168.1.100'  # 网关 PACS 系统的 IP 地址
    # gateway_pacs_port = 104  # 网关 PACS 系统的 DICOM 端口
    #
    # dicom_sender = DicomSender(dcm4che_path)
    # dicom_sender.send_multiple_dicom_series(series_dirs, gateway_pacs_aet, gateway_pacs_ip, gateway_pacs_port)

