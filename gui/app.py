import sys
import logging
from PyQt6.QtWidgets import QApplication
from gui import RemoteControllerWindow, TextHandler
from config import LOG_FILE


def start_gui():
    app = QApplication(sys.argv)
    window = RemoteControllerWindow()
    file_handler = logging.FileHandler(filename=LOG_FILE, mode="w", encoding="utf-8")
    app_handler = TextHandler(window.log_output)
    logging.basicConfig(format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
                        datefmt="%d-%m-%Y %H:%M:%S",
                        level=logging.INFO,
                        handlers=[file_handler, app_handler])
    sys.stdout = TextHandler(window.log_output)

    sys.exit(app.exec())
