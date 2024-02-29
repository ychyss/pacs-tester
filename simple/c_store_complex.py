from pynetdicom import AE, debug_logger, StoragePresentationContexts
from pynetdicom.sop_class import CTImageStorage, VLWholeSlideMicroscopyImageStorage
from pydicom.uid import JPEGBaseline8Bit
from pydicom import dcmread
import os
from datetime import datetime


def store_one_series(ae_title='HYS-LAPTOP', scp_address=('172.16.75.155', 30531), scp_ae_title="CONSULTATION", folder_path='../test_data/Ankle'):
    # 启用详细日志记录
    # debug_logger()

    # 创建一个应用实体
    ae = AE(ae_title=ae_title)

    # 添加 CTImageStorage 请求上下文
    ae.requested_contexts = StoragePresentationContexts
    # ae.add_requested_context(VLWholeSlideMicroscopyImageStorage, JPEGBaseline8Bit)

    # 连接到 SCP
    # scp_address = ('192.168.1.200', 11112)
    assoc = ae.associate(*scp_address, ae_title=scp_ae_title)
    if assoc.is_established:
        # 指定包含 DICOM 文件的文件夹

        # 记录发送开始时间
        start_time = datetime.now()

        # 遍历文件夹中的所有文件
        for filename in os.listdir(folder_path):
            filename1 = filename.lower()
            if filename1.endswith('.dcm'):  # 确保是 DICOM 文件
                file_path = os.path.join(folder_path, filename)
                ds = dcmread(file_path, force=True)
                if not hasattr(ds.file_meta, 'TransferSyntaxUID'):
                    ds.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'
                # 发送 C-STORE 请求
                status = assoc.send_c_store(ds)
                if status:
                    print(f'C-STORE response received for {filename}, status:', status)

        # 记录发送结束时间
        end_time = datetime.now()

        print(f'Total time taken for sending series: {end_time - start_time}')

        # 释放连接
        assoc.release()
    else:
        if assoc.is_rejected:
            print(f"Association rejected: {assoc.rejected_permanent_or_transient}")
        elif assoc.is_aborted:
            print("Association aborted by the server")
        else:
            print("Association failed for an unknown reason")


if __name__ == '__main__':
    root_dir = "D:\\images\\slide"
    # root_dir = "D:\\images\\中傣医院数据\\problem"

    patient_num = 0
    study_num = 0
    series_num = 0

    for patient in os.listdir(root_dir):
        patient_dir = os.path.join(root_dir, patient)
        patient_num = patient_num + 1
        # print("patient:", patient_dir)
        for study in os.listdir(patient_dir):
            study_dir = os.path.join(patient_dir, study)
            # print("study:", study_dir)
            study_num = study_num + 1
            for series in os.listdir(study_dir):
                series_dir = os.path.join(study_dir, series)
                print("series:", series_dir)
                for root, dirs, files in os.walk(series_dir):
                    if len(files) > 0:
                        print(f'发送{patient}的序列(StudyInstanceUID:{study}, SeriesInstanceUID:{series})...')
                        series_num = series_num + 1
                        store_one_series(scp_address=('172.16.75.155', 32704), scp_ae_title="DCM4CHEE", folder_path=root)
                        print('发送完成')

    print(f"共{patient_num}个患者，共{study_num}个检查，共{series_num}个序列")
