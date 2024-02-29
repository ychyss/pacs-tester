from c_find import do_find_studies_by_modality, do_find_patient_by_id
import pymysql


def find_diff():
    conn = pymysql.connect(host='172.16.50.66', user='5g_user', password='ry.5g_pro', database='rxpacs', port=3308)

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM 5g_pro_report')

    result = cursor.fetchall()
    result = list(result)
    diff = 0
    diff_record = []
    for record in result:
        image = do_find_patient_by_id('HYS-LAPTOP', '172.16.75.155', 32704, "DCM4CHEE", record[0])
        if len(image) > 0:
            print(f'{record[1]}({record[0]})找到影像{image}')
        else:
            diff = diff + 1
            diff_record.append(record)
    print(f'缺少影像的记录({diff}):\n{diff_record}')


if __name__ == '__main__':
    find_diff()
