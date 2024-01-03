from pydicom.dataset import Dataset
import threading
from pynetdicom import AE, evt, build_role, debug_logger
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelGet,
    CTImageStorage
)


class DICOMGetRetrieve:
    def __init__(self, calling_ae, scp_host, scp_port, scp_ae_title):
        self.calling_ae = calling_ae
        self.scp_host = scp_host
        self.scp_port = scp_port
        self.scp_ae_title = scp_ae_title
        self.image_received = threading.Event()
        self.result_ds = None

    def handle_store(self, event):
        """Handle a C-STORE request event."""

        self.result_ds = event.dataset
        self.result_ds.file_meta = event.file_meta
        # Save the dataset using the SOP Instance UID as the filename
        # ds.save_as(ds.SOPInstanceUID, write_like_original=False)

        # 标记图像已接收
        self.image_received.set()
        # Return a 'Success' status
        return 0x0000

    def do_get_instance(self, pid, studyid, ssid, sopid, sop_cls_uid):
        """

        :param pid:
        :param studyid:
        :param ssid:
        :param sopid:
        :param sop_cls_uid:
        :return:
        """
        ae = AE(self.calling_ae)
        ae.add_requested_context(PatientRootQueryRetrieveInformationModelGet)
        ae.add_requested_context(sop_cls_uid)

        handlers = [(evt.EVT_C_STORE, self.handle_store)]
        role = build_role(sop_cls_uid, scp_role=True)

        ds = Dataset()
        ds.QueryRetrieveLevel = 'IMAGE'
        ds.PatientID = pid
        ds.StudyInstanceUID = studyid
        ds.SeriesInstanceUID = ssid
        ds.SOPInstanceUID = sopid

        assoc = ae.associate(self.scp_host, self.scp_port, ae_title=self.scp_ae_title, ext_neg=[role], evt_handlers=handlers)
        try:
            if assoc.is_established:
                responses = assoc.send_c_get(ds, PatientRootQueryRetrieveInformationModelGet)
                for (status, identifier) in responses:
                    if status:
                        print('C-GET query status: 0x{0:04x}'.format(status.Status))
                    else:
                        print('Connection timed out, was aborted or received invalid response')

                # 等待图像被接收
                self.image_received.wait()

                return self.result_ds
            else:
                print('Association rejected, aborted or never connected')
        except Exception as e:
            print(e)
            return None
        finally:
            # 释放联接
            assoc.release()


if __name__ == '__main__':
    calling = 'HYS-LAPTOP'
    scp_host = '192.168.1.200'
    scp_port = 30205
    scp_ae_title = "DCM4CHEE"
    pid = '123456'
    studyid = '1111.2222.3333.4445.20210811003743'
    ssid = '1.3.46.670589.33.1.63764453753942632000002.4783910794170731801'
    sopid = '1.3.46.670589.33.1.63764453840849602800001.4656080259000860486'

    retriever = DICOMGetRetrieve(calling, scp_host, scp_port, scp_ae_title)
    retriever.do_get_instance(pid, studyid, ssid, sopid, '1.2.840.10008.5.1.4.1.1.2')

