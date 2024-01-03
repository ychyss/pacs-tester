from pydicom.dataset import Dataset

from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind
from pynetdicom.sop_class import StudyRootQueryRetrieveInformationModelFind
from typing import List, Dict, Union


def do_find_patient(calling_ae,
                    scp_host, scp_port, scp_ae_title,
                    patient_birth_date: str) -> Union[List[Dict], None]:
    """

    :param calling_ae:
    :param scp_host:
    :param scp_port:
    :param scp_ae_title:
    :param patient_birth_date:
    :return: 字典列表，包括患者基本信息和检查数量
    """
    # debug_logger()
    ae = AE(calling_ae)
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

    # 这里给出的字段不仅仅是查询条件，还有预备填入的字段
    ds = Dataset()
    ds.SpecificCharacterSet = 'ISO_IR 100'
    ds.PatientBirthDate = patient_birth_date
    ds.QueryRetrieveLevel = 'PATIENT'

    ds.PatientID = '*'
    ds.PatientName = '*'
    ds.PatientSex = ''
    ds.NumberOfPatientRelatedStudies = 0

    assoc = ae.associate(scp_host, scp_port, ae_title=scp_ae_title)
    patients = []
    try:
        if assoc.is_established:
            responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
            for (status, identifier) in responses:
                if status:
                    print('C-FIND query status: 0x{0:04X}'.format(status.Status))
                    if identifier:
                        patients.append({
                            "PatientID": identifier.PatientID,
                            "PatientName": identifier.PatientName,
                            'PatientBirthDate': identifier.PatientBirthDate,
                            "PatientSex": identifier.PatientSex,
                            "NumberOfPatientRelatedStudies": identifier.NumberOfPatientRelatedStudies
                        })
                else:
                    print('Connection timed out, was aborted or received invalid response')

        else:
            print('Association rejected, aborted or never connected')
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        # Release the association
        assoc.release()

    return patients


def do_find_studies(calling_ae,
                    scp_host, scp_port, scp_ae_title,
                    patient_id: str) -> Union[List[Dict], None]:
    """

    :param calling_ae:
    :param scp_host:
    :param scp_port:
    :param scp_ae_title:
    :param patient_id:
    :return:
    """
    # debug_logger()

    ae = AE(calling_ae)
    ae.add_requested_context(StudyRootQueryRetrieveInformationModelFind)

    # 这里给出的字段不仅仅是查询条件，还有预备填入的字段
    # 这里给出的字段不仅仅是查询条件，还有预备填入的字段
    ds = Dataset()

    ds.SpecificCharacterSet = 'ISO_IR 100'
    ds.PatientID = patient_id
    ds.QueryRetrieveLevel = 'STUDY'

    ds.PatientName = ''
    ds.PatientAge = ''
    ds.PatientBirthDate = ''
    ds.PatientSex = ''
    ds.StudyInstanceUID = ''
    ds.StudyID = ''
    ds.StudyDate = ''
    ds.StudyTime = ''
    ds.StudyDescription = ''
    ds.AccessionNumber = ''
    ds.ModalitiesInStudy = ""
    ds.NumberOfStudyRelatedSeries = 0

    assoc = ae.associate(scp_host, scp_port, ae_title=scp_ae_title)
    studies = []
    try:
        if assoc.is_established:
            # Send the C-FIND request
            responses = assoc.send_c_find(ds, StudyRootQueryRetrieveInformationModelFind)
            for (status, identifier) in responses:
                if status:
                    print('C-FIND query status: 0x{0:04X}'.format(status.Status))
                    if identifier:
                        studies.append({
                            'PatientID': identifier.PatientID,
                            'PatientName': identifier.PatientName,
                            'PatientBirthDate': identifier.PatientBirthDate,
                            'PatientAge': identifier.PatientAge,
                            'PatientSex': identifier.PatientSex,
                            "StudyInstanceUID": identifier.StudyInstanceUID,
                            'StudyID': identifier.StudyID,
                            'StudyDate': identifier.StudyDate,
                            'StudyTime': identifier.StudyTime,
                            'StudyDescription': identifier.StudyDescription,
                            'AccessionNumber': identifier.AccessionNumber,
                            "SOPClassesInStudy": identifier.ModalitiesInStudy,
                            'NumberOfStudyRelatedSeries': identifier.NumberOfStudyRelatedSeries
                        })
                else:
                    print('Connection timed out, was aborted or received invalid response')

        else:
            print('Association rejected, aborted or never connected')
    except Exception as e:
        print(e)
        return None
    finally:
        # Release the association
        assoc.release()

    return studies


def do_find_series(calling_ae,
                   scp_host, scp_port, scp_ae_title,
                   patient_id: str, study_ins_uid: str) -> Union[List[Dict], None]:
    """

    :param patient_id:
    :param calling_ae:
    :param scp_host:
    :param scp_port:
    :param scp_ae_title:
    :param study_ins_uid:
    :return:
    """
    # debug_logger()

    ae = AE(calling_ae)
    ae.add_requested_context(StudyRootQueryRetrieveInformationModelFind)

    ds = Dataset()
    ds.SpecificCharacterSet = 'ISO_IR 100'
    ds.PatientID = patient_id
    ds.StudyInstanceUID = study_ins_uid
    ds.QueryRetrieveLevel = 'SERIES'

    ds.PatientName = ''
    ds.PatientAge = ''
    ds.PatientBirthDate = ''
    ds.PatientSex = ''
    ds.StudyID = ''
    ds.StudyDate = ''
    ds.StudyTime = ''
    ds.StudyDescription = ''
    ds.AccessionNumber = ''
    ds.SeriesInstanceUID = ''
    ds.SeriesDate = ''
    ds.SeriesTime = ''
    ds.SeriesDescription = ''
    ds.Modality = ''
    # ds.SeriesNumber = 0
    ds.NumberOfSeriesRelatedInstances = 0
    ds.BodyPartExamined = ''
    ds.Manufacturer = ''
    ds.InstitutionName = ''
    ds.StationName = ''

    assoc = ae.associate(scp_host, scp_port, ae_title=scp_ae_title)
    series = []
    try:
        if assoc.is_established:
            # Send the C-FIND request
            responses = assoc.send_c_find(ds, StudyRootQueryRetrieveInformationModelFind)
            for (status, identifier) in responses:
                if status:
                    print('C-FIND query status: 0x{0:04X}'.format(status.Status))
                    if identifier:
                        series.append({
                            'PatientID': identifier.PatientID,
                            'PatientName': identifier.PatientName,
                            'PatientBirthDate': identifier.PatientBirthDate,
                            'PatientAge': identifier.PatientAge,
                            'PatientSex': identifier.PatientSex,
                            "StudyInstanceUID": identifier.StudyInstanceUID,
                            'StudyID': identifier.StudyID,
                            'StudyDate': identifier.StudyDate,
                            'StudyTime': identifier.StudyTime,
                            'StudyDescription': identifier.StudyDescription,
                            'AccessionNumber': identifier.AccessionNumber,
                            'SeriesInstanceUID': identifier.SeriesInstanceUID,
                            'SeriesDate': identifier.SeriesDate,
                            'SeriesTime': identifier.SeriesTime,
                            'SeriesDescription': identifier.SeriesDescription,
                            'Modality': identifier.Modality,
                            'NumberOfSeriesRelatedInstances': identifier.NumberOfSeriesRelatedInstances,
                            'BodyPartExamined': identifier.BodyPartExamined,
                            'Manufacturer': identifier.Manufacturer,
                            'InstitutionName': identifier.InstitutionName,
                            'StationName': identifier.StationName
                        })
                else:
                    print('Connection timed out, was aborted or received invalid response')

        else:
            print('Association rejected, aborted or never connected')
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        # Release the association
        assoc.release()

    return series


def do_find_instances(calling_ae,
                      scp_host, scp_port, scp_ae_title,
                      patient_id: str, study_ins_uid: str, series_ins_uid: str) -> Union[List[Dict], None]:
    """

    :param study_ins_uid:
    :param patient_id:
    :param calling_ae:
    :param scp_host:
    :param scp_port:
    :param scp_ae_title:
    :param series_ins_uid:
    :return:
    """
    ae = AE(calling_ae)
    ae.add_requested_context(StudyRootQueryRetrieveInformationModelFind)

    ds = Dataset()
    ds.SpecificCharacterSet = 'ISO_IR 100'
    ds.PatientID = patient_id
    ds.StudyInstanceUID = study_ins_uid
    ds.SeriesInstanceUID = series_ins_uid
    ds.QueryRetrieveLevel = 'IMAGE'

    ds.PatientName = ''
    ds.PatientAge = ''
    ds.PatientBirthDate = ''
    ds.PatientSex = ''
    ds.StudyID = ''
    ds.StudyDate = ''
    ds.StudyTime = ''
    ds.StudyDescription = ''
    ds.AccessionNumber = ''
    ds.SeriesDate = ''
    ds.SeriesTime = ''
    ds.SeriesDescription = ''
    ds.Modality = ''
    ds.BodyPartExamined = ''
    ds.Manufacturer = ''
    ds.InstitutionName = ''
    ds.StationName = ''
    ds.SOPInstanceUID = ''
    ds.Rows = 0
    ds.Columns = 0
    ds.BitsAllocated = 0
    ds.PerformedProcedureStepStartDate = ''
    ds.PerformedProcedureStepStartTime = ''

    assoc = ae.associate(scp_host, scp_port, ae_title=scp_ae_title)
    instances = []
    try:
        if assoc.is_established:
            # Send the C-FIND request
            responses = assoc.send_c_find(ds, StudyRootQueryRetrieveInformationModelFind)
            for (status, identifier) in responses:
                if status:
                    print('C-FIND query status: 0x{0:04X}'.format(status.Status))
                    if identifier:
                        instances.append({
                            'PatientID': identifier.PatientID,
                            'PatientName': identifier.PatientName,
                            'PatientBirthDate': identifier.PatientBirthDate,
                            'PatientAge': identifier.PatientAge,
                            'PatientSex': identifier.PatientSex,
                            "StudyInstanceUID": identifier.StudyInstanceUID,
                            'StudyID': identifier.StudyID,
                            'StudyDate': identifier.StudyDate,
                            'StudyTime': identifier.StudyTime,
                            'StudyDescription': identifier.StudyDescription,
                            'AccessionNumber': identifier.AccessionNumber,
                            'SeriesInstanceUID': identifier.SeriesInstanceUID,
                            'SeriesDate': identifier.SeriesDate,
                            'SeriesTime': identifier.SeriesTime,
                            'SeriesDescription': identifier.SeriesDescription,
                            'Modality': identifier.Modality,
                            'BodyPartExamined': identifier.BodyPartExamined,
                            'Manufacturer': identifier.Manufacturer,
                            'InstitutionName': identifier.InstitutionName,
                            'StationName': identifier.StationName,
                            'SOPInstanceUID': identifier.SOPInstanceUID,
                            'Rows': identifier.Rows,
                            'Columns': identifier.Columns,
                            'BitsAllocated': identifier.BitsAllocated,
                            'PerformedProcedureStepStartDate': identifier.PerformedProcedureStepStartDate,
                            'PerformedProcedureStepStartTime': identifier.PerformedProcedureStepStartTime
                        })
                else:
                    print('Connection timed out, was aborted or received invalid response')

        else:
            print('Association rejected, aborted or never connected')
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        # Release the association
        assoc.release()

    return instances


if __name__ == '__main__':
    birth_date = '19421012'
    calling = 'HYS-LAPTOP'
    scp_host = '172.16.75.155'
    scp_port = 32704
    scp_ae_title = "DCM4CHEE"
    
    pp = do_find_patient(calling, scp_host, scp_port, scp_ae_title, birth_date)
    print("patients:", pp)
    if len(pp) > 0:
        ss = do_find_studies(calling, scp_host, scp_port, scp_ae_title, pp[0]['PatientID'])
        print("studies:", ss)

        if len(ss) > 0:
            get_series = do_find_series(calling, scp_host, scp_port, scp_ae_title,
                                        pp[0]['PatientID'], ss[0]['StudyInstanceUID'])
            print("series:", get_series)

            if len(get_series) > 0:
                for se in get_series:
                    get_instances = do_find_instances(calling, scp_host, scp_port, scp_ae_title,
                                                      pp[0]['PatientID'], ss[0]['StudyInstanceUID'], se['SeriesInstanceUID'])
                    print('instances:', get_instances)

