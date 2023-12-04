from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import CTImageStorage, VLWholeSlideMicroscopyImageStorage
from pydicom.uid import JPEGBaseline8Bit
from pydicom import dcmread
import os
from datetime import datetime

# 启用详细日志记录
# debug_logger()

# 创建一个应用实体
ae = AE()

# 添加 CTImageStorage 请求上下文
ae.add_requested_context(CTImageStorage)
ae.add_requested_context(VLWholeSlideMicroscopyImageStorage, JPEGBaseline8Bit)

# 连接到 SCP
# scp_address = ('192.168.1.200', 11112)
scp_address = ('172.16.75.155', 30531)
assoc = ae.associate(*scp_address)

if assoc.is_established:
    # 指定包含 DICOM 文件的文件夹
    folder_path = '../test_data/Ankle'  # 替换为实际的文件夹路径

    # 记录发送开始时间
    start_time = datetime.now()

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.dcm'):  # 确保是 DICOM 文件
            file_path = os.path.join(folder_path, filename)
            ds = dcmread(file_path)
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
