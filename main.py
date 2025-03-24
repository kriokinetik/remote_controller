import asyncio
from threading import Thread
from gui.app import start_gui
from bot import TelegramBot
from tools.logger import logger_info, logger_error


def main():
    bot = TelegramBot()
    try:
        loop = asyncio.new_event_loop()
        Thread(target=bot.async_run, args=(loop,), daemon=True).start()
        start_gui()
    except KeyboardInterrupt:
        logger_info("Program interrupted by the user")
    except Exception as e:
        logger_error(f"Unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
