from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import Verification
from pydicom.uid import JPEGBaseline8Bit
from pydicom import dcmread
import os
from datetime import datetime

# 启用详细日志记录
# debug_logger()

# 创建一个应用实体
ae = AE(ae_title="HYS-LAPTOP")

# 添加 CTImageStorage 请求上下文
ae.add_requested_context(Verification)

# 连接到 SCP
# scp_address = ('222.197.200.248', 30531)
# scp_address = ('172.16.75.155', 30531)
scp_address = ('172.16.75.177', 30531)
assoc = ae.associate(*scp_address)

if assoc.is_established:

    # 记录发送开始时间
    start_time = datetime.now()

    # 发送 C-STORE 请求
    status = assoc.send_c_echo(666)

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
