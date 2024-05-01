try:
    import requests as requests
except ModuleNotFoundError:
    import urequests as requests
import yaml

config = yaml.safe_load(open("config.yaml"))


def ota_file(file: str) -> None:
    result = requests.get(config["OTA_URL_Prefix"].format(file))
    with open(file, "wb") as f:
        f.write(result.content)
    return


def ota_updater():
    if config["OTA_Disable"]:
        print("OTA Is disabled")
        return
    print("Downloading file list and templates")
    ota_file("OTA_Files/templates.yaml")
    ota_file("OTA_Files/main.py")
    ota_file("OTA_Files/utils.py")
    ota_file("utils.py")
    FILES = yaml.safe_load(open("OTA_Files/templates.yaml"))["FILES"]
    print("Updating Files")
    for file in FILES:
        print("Updating", file)
        ota_file("OTA_Files/" + file)
