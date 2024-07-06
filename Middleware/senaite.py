import sys
import os
import requests
import json
import configparser
from PySide6.QtWidgets import QApplication, QMessageBox

# load the cookie.ini file values
cookie_config = configparser.ConfigParser()
cookie_config.read(os.path.join(os.path.dirname(__file__), "..", "cookie.ini"))


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


def readJsonSenaiteSettings():
    filepath = os.path.join(os.path.dirname(__file__), "..", "settings.json")

    data_to_be_unpack = []
    senaite_data = None
    count = 0

    with open(filepath, "r") as jsonfile:
        json_data = json.load(jsonfile)

    if json_data:
        for analyzer in json_data:
            if count == 0:  # using count to get only the first element
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


# SENAITE.JSONAPI route
API_BASE_URL = "/@@API/senaite/v1"

# server, port, site, username, password = readJsonSenaiteSettings("")
data_unpack = readJsonSenaiteSettings()
server = None
port = None
site = None
if data_unpack:
    server, port, site = data_unpack

SENAITE_API_URL = f"http://{server}:{port}/{site}/{API_BASE_URL}"


def client_uid_path(sample_id):
    try:
        client_uid = ''

        # base_url = f"http://localhost:8080/senaite{API_BASE_URL}"
        resp = requests.get(f'{SENAITE_API_URL}/search', params={'id': sample_id}, cookies={cookie_config["Cookie"]["name"]: cookie_config["Cookie"]["value"]})
        analysis_path = resp.json()
        analysis_path = analysis_path['items']
        if resp.status_code == 200 and analysis_path:
            client_uid = analysis_path[0]['path']
        else:
            print("Sample ID doesn't exist in SENAITE!")
            show_message_box("Information", "SENAITE Error", "Sample ID doesn't exist in SENAITE!")

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

    try:
        resp = requests.get(f'{SENAITE_API_URL}/AnalysisService/', params={'limit': '50', 'review_state': 'active', 'complete': 'true'},
                            cookies={cookie_config["Cookie"]["name"]: cookie_config["Cookie"]["value"]})
        data = resp.json()
        data = data["items"]

        analysis_services = {}

        if resp.status_code == 200 and data:
            for i in range(len(data)):
                analysis_services.update({data[i]['ShortTitle']: data[i]['Keyword']})
        else:
            raise Exception("Unexpected error occurred while connecting to SENAITE.\n Provide the correct host address")

        print(analysis_services)
        # return analysis_services
    except Exception as e:
        show_message_box("Critical", "Error", str(e))


# function to return the path of the sample from SENAITE
def get_analysis_service():
    # ask the user for the senaite api url
    # base_url = f"http://localhost:8080/senaite{API_BASE_URL}"
    # af_url = "http://10.5.50.43:8091/agogo-test/@@API/senaite/v1"
    try:
        resp = requests.get(f'{SENAITE_API_URL}/AnalysisService/', params={'limit': '50', 'review_state': 'active', 'complete': 'true'},
                            cookies={cookie_config["Cookie"]["name"]: cookie_config["Cookie"]["value"]}, timeout=15)
        data = resp.json()
        data = data["items"]

        analysis_services = {}

        if resp.status_code == 200 and data:
            for i in range(len(data)):
                analysis_services.update({data[i]['ShortTitle'].upper(): data[i]['Keyword']})
        else:
            raise Exception("Unexpected error occurred while connecting to SENAITE.\n Provide the correct host address")

        # print(json.dumps(analysis_services, indent=4))
        return analysis_services

    except Exception as e:
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

    if len(analyzer_result) == 1:

        # print(analyzer_result[0])
        response = requests.post(f"{SENAITE_API_URL}/update", headers=headers, json=analyzer_result[0],
                                 cookies={cookie_config["Cookie"]["name"]: cookie_config["Cookie"]["value"]})

        # Handling the response from the server
        if response.status_code == requests.codes.ok:
            pass
            # print('Transfer was successful')
            # print(response.json())
        else:
            show_message_box("Information", "Transfer of Result", f"Transfer failed with status code: {response.status_code}.\n"
                                                                  f"The transfer result already exit in SENAITE LIMS!")
            # print('Request failed with status code:', response.status_code)

    else:
        tcd = ''
        for results in analyzer_result:
            # send the post request
            # json_str = json.dumps(result)
            response = requests.post(f"{SENAITE_API_URL}/update", headers=headers, json=results,
                                     cookies={cookie_config["Cookie"]["name"]: cookie_config["Cookie"]["value"]})

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
            show_message_box("Information", "Transfer of Result", f"Transfer failed with status code: {tcd}.\n"
                                                                  f"The transfer result already exist in SENAITE LIMS!")


# Transfer failed with status code: 401

if __name__ == '__main__':
    get_sample_path()
    get_analysis_service()
