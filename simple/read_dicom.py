import pydicom

def read_dicom():
    # 替换为您的DICOM文件路径
    dicom_file_path = 'C:/Users/HYS/Downloads/DICOM(1)/DICOM/CT.1.2.840.113704.9.1000.16.2.20201018152450447000400050001.DCM'
    # dicom_file_path = "D:/images/PET-CT/20210817001602/201/1_0.dcm"
    # 读取DICOM文件
    ds = pydicom.dcmread(dicom_file_path, force=True)

    # 打印一些基本信息
    print("Patient's Name:", ds.get('PatientName', 'Unknown'))
    print("Patient ID:", ds.get('PatientID', 'Unknown'))
    print("Modality:", ds.get('Modality', 'Unknown'))
    print("Study Date:", ds.get('StudyDate', 'Unknown'))

    if not hasattr(ds.file_meta, "TransferSyntaxUID"):
        ds.file_meta.TransferSyntaxUID = "1.2.840.10008.1.2"

    print(ds.file_meta.TransferSyntaxUID)
    # 如果想查看更多信息，可以尝试打印整个数据集
    # print(ds)


if __name__ == '__main__':
    read_dicom()

