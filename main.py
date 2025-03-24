import asyncio
import logging
import sys
from threading import Thread
from PyQt6.QtWidgets import QApplication
from gui import RemoteControllerWindow, TextHandler
from bot import run_bot, start_async_loop
from bot.logger import logger_info, logger_error
from config_reader import LOG_FILE


def main():
    app = QApplication(sys.argv)
    window = RemoteControllerWindow()
    file_handler = logging.FileHandler(filename=LOG_FILE, mode='w', encoding='utf-8')
    app_handler = TextHandler(window.log_output)
    logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S',
                        level=logging.INFO,
                        handlers=[file_handler, app_handler])
    sys.stdout = TextHandler(window.log_output)

    try:
        loop = asyncio.new_event_loop()
        Thread(target=start_async_loop, args=(loop,), daemon=True).start()
        # window.show()
        sys.exit(app.exec())
    except KeyboardInterrupt:
        logger_info('Program interrupted by the user')
    except Exception as e:
        logger_error(f'Unexpected error: {e}', exc_info=True)

if __name__ == '__main__':
    main()