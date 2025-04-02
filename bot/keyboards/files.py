from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import buttons


def next_directory(folders: list[str], pages: bool = False) -> InlineKeyboardMarkup:
    """
    Формирует клавиатуру при перемещении из одной директории в другую.

    :param folders: Список имен папок в текущей директории.
    :param pages: Если у директории слишком много файлов len(message) > 4096
    :return: InlineKeyboardMarkup с кнопками для перехода в следующую директорию.
    """

    keyboard = []

    if pages:
        keyboard.append([
            buttons.files.prev_page,
            buttons.files.next_page
        ])

    # Добавляем кнопки для каждой папки в текущей директории
    for folder_name in folders:
        # Если имя папки длиннее 30 символов, обрезаем его для отображения на кнопке
        displayed_name = f"{folder_name[:30]}...\\" if len(folder_name) > 30 else folder_name
        keyboard.append([InlineKeyboardButton(text=displayed_name, callback_data=folder_name)])

    keyboard.append([
        buttons.files.parent_directory,
        buttons.files.desktop,
        buttons.files.disk_C,
        buttons.files.disk_D
    ])

    keyboard.append([buttons.home.main_button])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_progress_keyboard(text: str, url: str = None) -> InlineKeyboardMarkup:
    if url:
        progress_button = [[InlineKeyboardButton(text=text, url=url)]]
    else:
        progress_button = [[InlineKeyboardButton(text=text, callback_data="*")]]

    return InlineKeyboardMarkup(inline_keyboard=progress_button)
