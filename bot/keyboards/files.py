from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import buttons


def get_files_manager_keyboard(mode: str, pages: bool = False) -> InlineKeyboardMarkup:
    """
    Формирует клавиатуру при перемещении из одной директории в другую.

    :param pages: Если у директории слишком много файлов len(message) > 4096
    :param mode: Текущий режим вывода (папки/файлы).
    :return: InlineKeyboardMarkup с кнопками для перехода в следующую директорию.
    """

    keyboard = []

    if pages:
        keyboard.append([buttons.files.prev_page, buttons.files.next_page])

    if mode == "folder":
        keyboard.append([buttons.files.show_files])
    elif mode == "file":
        keyboard.append([buttons.files.show_folders])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_progress_keyboard(text: str, url: str = None) -> InlineKeyboardMarkup:
    if url:
        progress_button = [[InlineKeyboardButton(text=text, url=url)]]
    else:
        progress_button = [[InlineKeyboardButton(text=text, callback_data="*")]]

    return InlineKeyboardMarkup(inline_keyboard=progress_button)
