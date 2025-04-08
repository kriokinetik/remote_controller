import json


def get_config() -> {}:
    try:
        with open(CONFIG_FILE) as f:
            data = json.load(f)

        config = {
            "token": data.get("TOKEN", ""),
            "admin": data.get("ADMIN", []),
            "yandex": {
                "token": data.get("YANDEX", {}).get("TOKEN", ""),
                "id": data.get("YANDEX", {}).get("ID", ""),
                "secret": data.get("YANDEX", {}).get("SECRET", "")
            }
        }
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(json.dumps({}, indent=4, ensure_ascii=False))
        return {}

    return config

# CONST
SCREENSHOT_NAME = "screenshot.png"
YANDEX_FOLDER = "remote_controller"
LOG_FILE = "remote_controller.log"
MISC_FOLDER = "./misc"
CONFIG_FILE = "config.json"
MAX_SIZE = 52428800
MAX_MESSAGE_LENGTH = 4096
PAGE_SIZE = 10
