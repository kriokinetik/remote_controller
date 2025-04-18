import sys
import os
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from PyQt6.QtWidgets import QApplication
from gui import MainWindow, TextHandler
from config import LOG_DIR


def configure_logging(window):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Форматирование имени файла с датой
    log_filename = datetime.now().strftime("log_%Y-%m-%d.log")
    log_file = os.path.join(LOG_DIR, log_filename)

    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=7,
        backupCount=50,
        encoding="utf-8"
    )

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
    window.show()

    configure_logging(window)

    sys.stdout = TextHandler(window.log_output)
    sys.stderr = TextHandler(window.log_output)

    window.start_bot_thread()

    sys.exit(app.exec())
