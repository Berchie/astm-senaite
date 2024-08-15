import os
import sys
import datetime
import re
from Middleware.senaite import client_uid_path, get_analysis_service, transfer_to_senaite, show_message_box
from Middleware.sqlite_db import insert_record, create_db_table


# using data files
# finding them using the code below
def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
        return os.path.join(datadir, "data", filename)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, "..", "data", filename)


basedir = os.path.dirname(__file__)


def parse_astm_data(astm_data):
    try:
        records = astm_data.split('\n')
        # print(records)

        data = {"patients": []}
        results = {}
        dict_r = {"lab_results": []}
        order = None
        result = None
        analyzer = ""
        result_dict = []
        record_type = None
        fbc_path = None
        cs_path = None
        ch_path = None
        analysis_test_path = None
        date_performed = None
        take_first_date = 0

        # database file path
        # db_dir_path = find_data_file("result_astm.db")
        db_dir_path = os.path.join(basedir, "..", "data", "result_astm.db")

        # variables for sqlite parameters
        t_date = datetime.datetime.now()
        t_analyzer = None
        t_sampleid = None
        t_message = astm_data

        # analysis services keywords from senaite
        analysis_services = get_analysis_service()

        for record in records:
            fields = re.split(r'[|^\\]', record)
            # print(fields)

            # using list comprehension to remove empty strings from the fields list
            fields = [field for field in fields if field]
            # print(fields)

            """
                use a list comprehension to iterate through the elements in the list and apply the 
                encode('unicode-escape').decode('unicode-escape') method to each element to remove the hexadecimal escape codes.
            """
            fields = [field.encode('unicode-escape').decode('unicode-escape') for field in fields]
            # print(fields)

            # if the len of the record type is > 0 extract the last char
            if fields:  # check if fields is not empty or not None
                if len(fields[0]) > 1:
                    record_type = fields[0][-1]
                else:
                    record_type = fields[0]

            # record_type = fields[0]  #[-1]
            # print(record_type)

            if record_type == "H":
                analyzer = fields[2].strip()

                # assign the analyzer
                t_analyzer = analyzer.upper()

                # print(analyzer)

            match analyzer:
                case 'XN-330':  # Sysmex Haematology
                    if record_type == 'O':
                        fbc_path = client_uid_path(fields[2].strip())

                        analysis_test_path = fbc_path

                        # assign the sample id
                        t_sampleid = fields[2].strip()

                        # results.update({"path" : uid_path})

                    elif record_type == 'R':
                        # get the keywords from senaite and use it as the key for the result
                        # print(analysis_services.keys())
                        if fields[2] in analysis_services.keys():
                            keyword_ = analysis_services[fields[2]]
                            path_key = f'{fbc_path}/{keyword_}'
                            results.update({"path": path_key})
                            if fields[4] == "----":
                                fbc_value = 0
                            elif fields[4] == "W":
                                fbc_value = fields[5]
                            else:
                                fbc_value = fields[4]
                            results.update({"Result": float(fbc_value)})
                            results.update({"transition": "submit"})
                            result_dict.append(results.copy())

                        if fields[1] == "2":
                            # print(fields[7])
                            results.clear()
                            # date_performed = yyyy-mm-dd hh:mm
                            date_performed = f"{fields[8][0:12][0:4]}-{fields[8][0:12][4:6]}-{fields[8][0:12][6:8]} {fields[8][0:12][8:10]}:{fields[8][0:12][10:12]}"
                            # results.update({"path": analysis_test_path})
                            # results.update({"ClientOrderNumber": date_performed})  # getClientOrderNumber
                            # result_dict.append(results.copy())
                            # print(date_performed)

                case 'Becton Dickinson':  # BD Bactec FX40
                    if record_type == 'O':
                        # results.update({"id" : fields[2].strip()})
                        cs_path = client_uid_path(fields[2].strip())

                        # assign the sample id
                        t_sampleid = fields[2].strip()

                    elif record_type == 'R':
                        if fields[4] == "INST_NEGATIVE":
                            cs_result = 0
                        else:
                            cs_result = 1

                        cs_path_value = f"{cs_path}/{fields[2].strip()}"

                        results.update({"path": cs_path_value})
                        results.update({"Result": cs_result})
                        results.update({"transition": "submit"})
                        result_dict.append(results.copy())

                case _:  # cobass c111  chemistry analyzer
                    if record_type == 'O':
                        # results.update({"id" : fields[2].strip()})
                        ch_path = client_uid_path(fields[2].strip())

                        analysis_test_path = ch_path

                        # assign the sample id
                        t_sampleid = fields[2].strip()

                        if fields[1] == "1":
                            # print(fields[5])
                            results.clear()
                            # date_performed = yyyy-mm-dd hh:mm
                            date_performed = f"{fields[5][0:12][0:4]}-{fields[5][0:12][4:6]}-{fields[5][0:12][6:8]} {fields[5][0:12][8:10]}:{fields[5][0:12][10:12]}"
                            # results.update({"path": analysis_test_path})
                            # results.update({"ClientOrderNumber": date_performed})  # getClientOrderNumber
                            # result_dict.append(results.copy())

                    elif record_type == 'R':
                        # get the keywords from senaite and use it as the key for the result
                        if fields[2] in analysis_services.values():
                            ch_path_value = f"{ch_path}/{fields[2]}"
                            results.update({"path": ch_path_value})
                            results.update({"Result": fields[3]})
                            results.update({"transition": "submit"})
                            result_dict.append(results.copy())

            results.clear()

        # date of test was performed
        if date_performed:
            results.update({"path": analysis_test_path})
            results.update({"ClientOrderNumber": date_performed})  # getClientOrderNumber
            result_dict.append(results.copy())

        # insert record into the sqlite database
        t_message = t_message
        if os.path.exists(db_dir_path):
            insert_record(t_date, t_analyzer, t_sampleid, t_message)
        else:
            create_db_table()
            insert_record(t_date, t_analyzer, t_sampleid, t_message)

        # print(result_dict)
        return result_dict
    except Exception as e:
        show_message_box("Critical", "Parser Error", f"Error occurred: {str(e)}")


def astm_parser(textfile):
    with open(textfile, 'r') as file:
        result = file.read()

    data = parse_astm_data(result)

    print(data)
    transfer_to_senaite(data)


if __name__ == '__main__':
    astm_parser("C:\\Users\\berchie\\Downloads\\bactecfx.txt")
    # astm_parser('../demo_xn350.text')
