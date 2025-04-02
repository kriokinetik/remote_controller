import os
from dotenv import load_dotenv

load_dotenv()

# TELEGRAM
token = os.environ["TOKEN"]
admin = int(os.getenv("ADMIN"))

# YANDEX
yandex_token = os.environ["YANDEX_TOKEN"]
yandex_id = os.environ["YANDEX_ID"]
yandex_secret = os.environ["YANDEX_SECRET"]

# CONST
SCREENSHOT_NAME = "screenshot.png"
YANDEX_FOLDER = "remote_controller"
LOG_FILE = "remote_controller.log"
MISC_FOLDER = "./misc"
MAX_SIZE = 52428800
MAX_MESSAGE_LENGTH = 4096
PAGE_SIZE = 10
