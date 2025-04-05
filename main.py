from gui.app import start_gui
from tools.logger import logger_info, logger_error
from tools.file_ops import clear_misc_folder


def main():
    try:
        clear_misc_folder()
        start_gui()
    except KeyboardInterrupt:
        logger_info("Program interrupted by the user")
    except Exception as e:
        logger_error(f"Unexpected error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
