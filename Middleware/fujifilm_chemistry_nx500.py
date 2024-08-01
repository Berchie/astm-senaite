import os
import sys
import datetime
import re
# import json
# import requests
from Middleware.senaite import client_uid_path, get_analysis_service, transfer_to_senaite, show_message_box
from Middleware.sqlite_db import create_db_table, insert_record


# using data files
# finding them using the code below
# def find_data_file(filename):
#     if getattr(sys, "frozen", False):
#         # The application is frozen
#         datadir = os.path.dirname(sys.executable)
#         return os.path.join(datadir, "data", filename)
#     else:
#         # The application is not frozen
#         # Change this bit to match where you store your data files:
#         datadir = os.path.dirname(__file__)
#     return os.path.join(datadir, "..", "data", filename)


basedir = os.path.dirname(__file__)


def nx500_parser_data(result_data):
    chem_result = {}
    dict_chem_result = []
    # dp_test = None
    # dp_test_result = None
    analysis_path = ''

    # getting the analysis services keywords from SENAITE
    analysis_services = get_analysis_service()

    t_date = str(datetime.datetime.now())
    t_analyzer = 'NX-500'
    t_sampleid = None
    t_message = result_data

    # database file path
    # db_dir_path = find_data_file("result_astm.db")
    db_dir_path = os.path.join(basedir, "..", "data", "result_astm.db")

    try:
        # strip all extra tails
        records = result_data.strip()

        # split the data
        records = records.split(' ')

        # remove all empty string
        records = [data for data in records if data]

        # remove the lead two digit 02
        records = [re.sub("^[0-9][0-9]", "", nd) for nd in records]

        # remove or strip leading char '='
        records = [d.lstrip("=") for d in records]

        print(records)

        aPath = ''
        date_perform = ''

        for dp in range(len(records)):

            if dp == 2:
                analysis_path = client_uid_path(records[dp])

                aPath = analysis_path

                # assign sampleid
                t_sampleid = records[dp]

            match dp:
                case 1:
                    date_perform = records[dp]
                case 3:
                    dp_test = f"{analysis_path}/{analysis_services[records[dp].upper()]}"
                    chem_result.update({"path": dp_test})
                case 4:
                    dp_test_result = float(records[dp])
                    chem_result.update({"Result": dp_test_result})
                    chem_result.update({"transition": "submit"})
                    dict_chem_result.append(chem_result.copy())
                case 6:
                    dp_test = f"{analysis_path}/{analysis_services[records[dp].upper()]}"
                    chem_result.update({"path": dp_test})
                case 7:
                    dp_test_result = float(records[dp])
                    chem_result.update({"Result": dp_test_result})
                    chem_result.update({"transition": "submit"})
                    dict_chem_result.append(chem_result.copy())
                case 9:
                    dp_test = f"{analysis_path}/{analysis_services[records[dp].upper()]}"
                    chem_result.update({"path": dp_test})
                case 10:
                    dp_test_result = float(records[dp])
                    chem_result.update({"Result": dp_test_result})
                    chem_result.update({"transition": "submit"})
                    dict_chem_result.append(chem_result.copy())
                case 12:
                    dp_test = f"{analysis_path}/{analysis_services[records[dp].upper()]}"
                    chem_result.update({"path": dp_test})
                case 15:
                    dp_test_result = float(records[dp])
                    chem_result.update({"Result": dp_test_result})
                    chem_result.update({"transition": "submit"})
                    dict_chem_result.append(chem_result.copy())
                case 16:
                    dp_test = f"{analysis_path}/{analysis_services[records[dp].upper()]}"
                    chem_result.update({"path": dp_test})
                case 17:
                    dp_test_result = float(records[dp])
                    chem_result.update({"Result": dp_test_result})
                    chem_result.update({"transition": "submit"})
                    dict_chem_result.append(chem_result.copy())

        chem_result.clear()
        # date of test was performed
        if date_perform:
            dp_date = f"20{date_perform[:8]} {date_perform[8:13]}"
            chem_result.update({"path": aPath})
            chem_result.update({"ClientOrderNumber": dp_date})
            dict_chem_result.append(chem_result.copy())

        # inserting the record into db
        if os.path.exists(db_dir_path):
            insert_record(t_date, t_analyzer, t_sampleid, t_message)
        else:
            create_db_table()
            insert_record(t_date, t_analyzer, t_sampleid, t_message)

        # return the processed data
        return dict_chem_result

    # print(records)
    except Exception as e:
        show_message_box("Critical", "Error", f"Error while process the result {e}")


def fujifilm_astm_parser(textfile):
    with open(textfile, 'r') as file:
        result = file.read()

    data = nx500_parser_data(result)

    print(data)
    transfer_to_senaite(data)


if __name__ == '__main__':
    fujifilm_astm_parser("../output_file.txt")
