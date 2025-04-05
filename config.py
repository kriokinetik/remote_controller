import json


def get_config() -> {}:
    with open("config.json") as f:
        data = json.load(f)

    config = {
        "token": data["TOKEN"],
        "admin": data["ADMIN"],
        "yandex": {
            "token": data["YANDEX"]["TOKEN"],
            "id": data["YANDEX"]["ID"],
            "secret": data["YANDEX"]["SECRET"]
        }
    }

    return config

# CONST
SCREENSHOT_NAME = "screenshot.png"
YANDEX_FOLDER = "remote_controller"
LOG_FILE = "remote_controller.log"
MISC_FOLDER = "./misc"
MAX_SIZE = 52428800
MAX_MESSAGE_LENGTH = 4096
PAGE_SIZE = 10
