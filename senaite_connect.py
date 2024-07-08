import sys
import os
import configparser
import json
import requests
from PySide6.QtWidgets import QApplication, QMessageBox


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


def read_json_senaite_settings():
    filepath = os.path.join(os.path.dirname(__file__), "settings.json")

    data_to_be_unpack = []
    senaite_data = None
    count = 0

    if os.path.getsize(filepath) > 0:
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
                    if key == "username":
                        data_to_be_unpack.append(senaite_data["username"])
                    if key == "password":
                        data_to_be_unpack.append(senaite_data["password"])

    return data_to_be_unpack


# SENAITE.JSONAPI route
API_BASE_URL = "/@@API/senaite/v1"

# data_unpack = readJsonSenaiteSettings()
#
# server = None
# port = None
# site = None
# username = None
# password = None
#
# if data_unpack:
#     server, port, site, username, password = data_unpack
#
# SENAITE_API_URL = f"http://{server}:{port}/{site}/{API_BASE_URL}"


def login_senaite_api():
    data_unpack = read_json_senaite_settings()

    server = None
    port = None
    site = None
    username = None
    password = None

    if data_unpack:
        server, port, site, username, password = data_unpack

    senaite_api_url = f"http://{server}:{port}/{site}/{API_BASE_URL}"

    try:
        reqs = requests.post(f"{senaite_api_url}/login", params={"__ac_name": username, "__ac_password": password}, timeout=15)

        # check if the response status is OK(200) and return data is not empty
        # before proceeding with writing the cookies to a file
        if reqs.status_code == 200 and reqs.json()["items"]:
            # print(json.dumps(reqs.json(), indent=2))

            # assigning cookies from the response header
            cookie = reqs.headers['Set-Cookie']

            # set a new the COOKIE NAME & COOKIE VALUE in ini file
            replace_cookie_name = cookie.replace(";", "=").split("=")[0]

            replace_cookie_value = cookie.replace(";", "=").split("=")[1]

            # create instance of the configparser
            config = configparser.ConfigParser()

            config_file_path = os.path.join(os.path.dirname(__file__), 'cookie.ini')

            # read the cookie.ini file
            config.read(config_file_path)

            # escape the '%'
            if '%' in replace_cookie_value:
                replace_cookie_value = replace_cookie_value.replace("%", "%%")

            # update the cookie.ini file
            config.set('Cookie', 'name', replace_cookie_name)
            config.set('Cookie', 'value', replace_cookie_value)

            # write or update the cookie.ini Cookie section
            with open(config_file_path, 'w') as configfile:
                config.write(configfile)
    except Exception as e:
        show_message_box("Critical", "Error", str(e))
        #print(str(e))


if __name__ == "__main__":
    login_senaite_api()
