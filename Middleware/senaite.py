import sys
import os
import json
import configparser
import requests
from PySide6.QtWidgets import QApplication, QMessageBox


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


# load the cookie.ini file values
cookie_file = find_data_file("cookie.ini")
cookie_config = configparser.ConfigParser()
cookie_config.read(cookie_file)

text_filepath = find_data_file("setting_names.txt")

stored_settings_name = ''


def show_message_box(level, title, message):
    # create an instance of QApplication if not already present
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # create an instance of QMessageBox
    message_box = QMessageBox()

    # set the title,text, Icon type, and add standard buttons
    message_box.setWindowTitle(title)
    message_box.setText(message)
    if str(level).capitalize() == "Critical":
        message_box.setIcon(QMessageBox.Critical)
    else:
        message_box.setIcon(QMessageBox.Information)
    message_box.setStandardButtons(QMessageBox.Ok)

    # show the message box
    message_box.exec()

    # clean the QApplication instance if created
    if not QApplication.instance():
        app.exit()


def process_settings_name(data_sn):
    global stored_settings_name
    stored_settings_name = data_sn
    # print(stored_settings_name)


def readTextFileSettings():
    with open(text_filepath, 'r') as tf:
        text_data = tf.read()

    return text_data.strip()


def read_json_senaite_settings(setting_name):
    filepath = find_data_file("settings.json")

    data_to_be_unpack = []
    senaite_data = None
    count = 0

    if os.path.getsize(filepath) > 0:
        with open(filepath, "r") as jsonfile:
            json_data = json.load(jsonfile)

        if json_data:
            for analyzer in json_data:
                if analyzer == setting_name:  # using count to get only the first element
                    senaite_data = json_data[analyzer]

                count += 1

            if senaite_data:
                for key in senaite_data:
                    if key == "server":
                        data_to_be_unpack.append(senaite_data["server"])
                    if key == "port":
                        data_to_be_unpack.append(senaite_data["port"])
                    if key == "site":
                        data_to_be_unpack.append(senaite_data["site"])
                    # if key == "username":
                    #     data_to_be_unpack.append(senaite_data["username"])
                    # if key == "password":
                    #     data_to_be_unpack.append(senaite_data["password"])

    return data_to_be_unpack


API_BASE_URL = "/@@API/senaite/v1"


def senaite_api_url():
    # SENAITE.JSONAPI route
    # API_BASE_URL = "/@@API/senaite/v1"
    SENAITE_API_URL = None
    data_unpack = None

    # server, port, site, username, password = readJsonSenaiteSettings("")
    if stored_settings_name:
        data_unpack = read_json_senaite_settings(stored_settings_name)
    server = None
    port = None
    site = None
    if data_unpack:
        server, port, site = data_unpack

    SENAITE_API_URL = f"http://{server}:{port}/{site}/{API_BASE_URL}"

    return SENAITE_API_URL


def client_uid_path(sample_id):
    senaite_url = senaite_api_url()
    try:
        client_uid = ''

        base_url = f"http://localhost:8080/senaite{API_BASE_URL}"
        resp = requests.get(f'{senaite_url}/search', params={'id': sample_id},
                            cookies={cookie_config["Cookie"]["name"]: cookie_config["Cookie"]["value"]}, timeout=15)
        analysis_path = resp.json()
        analysis_path = analysis_path['items']
        if resp.status_code == 200 and analysis_path:
            client_uid = analysis_path[0]['path']
        else:
            # print("Sample ID doesn't exist in SENAITE!")
            show_message_box("Information", "SENAITE Error", "Sample ID doesn't exist in SENAITE!")

        # print(client_uid)
    # except requests.exceptions.ConnectionError as ce:
    #     print('Connection error:', ce)
    # # Handle Timeout
    # except requests.exceptions.Timeout as te:
    #     print('Request timed out:', te)
    # # Handle HTTPError
    # except requests.exceptions.HTTPError as he:
    #     print('HTTP error occurred:', he)
    except Exception as e:
        show_message_box("Critical", "Error", str(e))
    else:
        # print(client_uid)
        return client_uid


# function to return the path of the sample from SENAITE
def get_sample_path():
    # ask the user for the senaite api url
    # base_url = f"http://localhost:8080/senaite{API_BASE_URL}"
    base_url = senaite_api_url()

    try:
        resp = requests.get(f'{base_url}/AnalysisService/',
                            params={'limit': '50', 'review_state': 'active', 'complete': 'true'},
                            cookies={cookie_config["Cookie"]["name"]: cookie_config["Cookie"]["value"]}, timeout=15)
        data_sp = resp.json()
        data_sp = data_sp["items"]

        analysis_services = {}

        if resp.status_code == 200 and data_sp:
            for i in range(len(data_sp)):
                analysis_services.update({data_sp[i]['ShortTitle']: data_sp[i]['Keyword']})
        else:
            show_message_box("Critical", "SENAITE Error", "Unexpected error occurred while connecting "
                                                          "to SENAITE.\nProvide the correct host address")
        # raise Exception("Unexpected error occurred while connecting to SENAITE.\n Provide the correct host address")

        print(analysis_services)
        # return analysis_services
    except Exception as e:
        show_message_box("Critical", "Error", str(e))


# function to return the path of the sample from SENAITE
def get_analysis_service():
    # ask the user for the senaite api url
    # base_url = f"http://localhost:8080/senaite{API_BASE_URL}"
    # af_url = "http://192.168.1.102:8099/demolims/@@API/senaite/v1"
    lims_apu_url = senaite_api_url()
    # lims_apu_url = af_url

    try:
        resp = requests.get(f'{lims_apu_url}/AnalysisService/',
                            params={'limit': '100', 'review_state': 'active', 'complete': 'true'},
                            cookies={cookie_config["Cookie"]["name"]: cookie_config["Cookie"]["value"]}, timeout=15)
        data_as = resp.json()
        data_as = data_as["items"]

        analysis_services = {}

        if resp.status_code == 200 and data_as:
            for i in range(len(data_as)):
                analysis_services.update({data_as[i]['ShortTitle'].upper(): data_as[i]['Keyword']})
        else:
            raise Exception("Unexpected error occurred while connecting to SENAITE.\n Provide the correct host address")

        # print(json.dumps(analysis_services, indent=4))
        return analysis_services

    except Exception as e:
        print(str(e))
        show_message_box("Critical", "Error", str(e))


# transfer the analyzer results to update SENAITE
def transfer_to_senaite(analyzer_result):
    transfer_count = 0
    transfer_err = 0

    # url of SENAITE to update analysis
    # senaite_url = f"http://10.5.50.44:8081/assinfoso-test/@@API/senaite/v1/update"
    # senaite_url = f"http://localhost:8080/senaite/@@API/senaite/v1/update"
    # Specify the appropriate header for the POST request
    headers = {'Content-type': 'application/json'}
    api_url_senaite = senaite_api_url()

    if len(analyzer_result) == 1:

        # print(analyzer_result[0])
        response = requests.post(f"{api_url_senaite}/update", headers=headers, json=analyzer_result[0],
                                 cookies={cookie_config["Cookie"]["name"]: cookie_config["Cookie"]["value"]},
                                 timeout=15)

        # Handling the response from the server
        if response.status_code == requests.codes.ok:
            pass
            # print('Transfer was successful')
            # print(response.json())
        else:
            show_message_box("Information", "Transfer of Result",
                             f"Transfer failed with status code: {response.status_code}.\n"
                             f"The transfer result already exit or not registered in SENAITE LIMS!")
            # print('Request failed with status code:', response.status_code)

    else:
        tcd = ''
        for results in analyzer_result:
            # send the post request
            # json_str = json.dumps(result)
            response = requests.post(f"{api_url_senaite}/update", headers=headers, json=results,
                                     cookies={cookie_config["Cookie"]["name"]: cookie_config["Cookie"]["value"]},
                                     timeout=15)

            # Handling the response from the server
            if response.status_code == requests.codes.ok:
                transfer_count += 1  # to count the successful transfer
                # print('Transfer of result was successful')
                # print(response.json())
            else:
                transfer_err += 1
                # print('Transfer failed with status code:', response.status_code)
                tcd = response.status_code

        if transfer_err > 0:
            show_message_box("Information", "Transfer of Result", f"Transfer failed with status code:"
                                                                  f"{tcd}.\nEither the transfer result already exist"
                                                                  f" or not registered in SENAITE LIMS!")


# Transfer failed with status code: 401

if __name__ == '__main__':
    # get_sample_path()
    # get_analysis_service()
    data = get_analysis_service()
    print(data)
