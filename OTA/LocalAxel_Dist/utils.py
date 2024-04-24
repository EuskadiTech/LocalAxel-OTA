try:
    import requests as requests
except ModuleNotFoundError:
    import urequests as requests
import config


def ota_file(file: str) -> None:
    result = requests.get(config.OTA_URL_Prefix.format(file))
    with open(file, "wb") as f:
        f.write(result.content)
    return


def ota_updater():
    if config.OTA_Disable:
        print("OTA Is disabled")
        return
    print("Downloading file list and templates")
    ota_file("templates.py")
    ota_file("main.py")
    ota_file("utils.py")
    FILES: list = __import__("templates").FILES
    print("Updating Files")
    for file in FILES:
        print("Updating", file)
        ota_file("static/" + file)