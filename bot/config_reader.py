import os
from dotenv import load_dotenv

load_dotenv()


token = os.environ['TOKEN']
admin = int(os.getenv('ADMIN'))

yandex_token = os.environ['YANDEX_TOKEN']
yandex_id = os.environ['YANDEX_ID']
yandex_secret = os.environ['YANDEX_SECRET']

# CONST
SCREENSHOT_NAME = 'screenshot.png'
YANDEX_FOLDER = 'remote_controller'
LOG_FILE = '../remote_controller.log'
MAX_SIZE = 52428800
