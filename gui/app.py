import sys
import logging
from PyQt6.QtWidgets import QApplication
from gui import MainWindow, TextHandler
from config import LOG_FILE


def configure_logging(window):
    file_handler = logging.FileHandler(filename=LOG_FILE, mode="a", encoding="utf-8")
    app_handler = TextHandler(window.log_output)

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.INFO,
        handlers=[file_handler, app_handler]
    )


def start_gui():
    app = QApplication(sys.argv)
    window = MainWindow()

    configure_logging(window)

    sys.stdout = TextHandler(window.log_output)
    sys.stderr = TextHandler(window.log_output)

    window.start_bot_thread()

    sys.exit(app.exec())
