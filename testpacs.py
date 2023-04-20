
from utils.pacs_util import modify_dicom_attributes
from utils.dicom_sender import DicomSender
from utils.dicom_manager import DicomManager


if __name__ == "__main__":
    # 生成随机数据
    input_directory = "./source_data/Head"
    output_directory = "./test_data/"
    number_of_series = 5  # Change this value to the desired number of series

    dicom_manager = DicomManager(input_directory, output_directory)
    # 生成
    # dicom_manager.generate_dicom_series(number_of_series)
    # 删除
    # dicom_manager.delete_dicom_series()
    # 获取
    series_dirs = dicom_manager.get_series_directories()
    if len(series_dirs) < 1:
        raise Exception("no test data")
    print(f"将要发送的序列({len(series_dirs)}): ", series_dirs)

    # 生成一个随机的UUID作为Study Instance UID

    # 批量发送到pacs 查看效果
    dcm4che_path = '../app/util/dcm4che-5.26.0/'
    gateway_pacs_aet = 'DCM_GATEWAY'  # 网关 PACS 系统的 AETitle
    gateway_pacs_ip = '192.168.1.200'  # 网关 PACS 系统的 IP 地址
    gateway_pacs_port = 32005  # 网l关 PACS 系统的 DICOM 端口, 这里是映射出来的端口

    dicom_sender = DicomSender(dcm4che_path)
    dicom_sender.send_multiple_dicom_series(series_dirs, gateway_pacs_aet, gateway_pacs_ip, gateway_pacs_port)


