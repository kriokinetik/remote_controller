from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import buttons


def next_directory(folders: list) -> InlineKeyboardMarkup:
    """
    Формирует клавиатуру при перемещении из одной директории в другую.

    :param folders: Список имен папок в текущей директории.
    :return: InlineKeyboardMarkup с кнопками для перехода в следующую директорию.
    """

    keyboard = []
    # Добавляем кнопки для каждой папки в текущей директории
    for folder_name in folders:
        # Если имя папки длиннее 32 символов, обрезаем его для отображения на кнопке
        displayed_name = f'{folder_name[:32]}...' if len(folder_name) > 32 else folder_name
        keyboard.append([InlineKeyboardButton(text=displayed_name, callback_data=folder_name)])
    # Добавляем кнопки для перехода к родительской директории и дискам C и D
    keyboard.append([buttons.retrieve_file.parent_directory, buttons.retrieve_file.disk_C, buttons.retrieve_file.disk_D])
    # Добавляем кнопку для возврата к главному меню
    keyboard.append([buttons.main_window.main_button])
    # Создаем и возвращаем Inline клавиатуру
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_progress_keyboard(text: str, url: str = None) -> InlineKeyboardMarkup:
    if url:
        progress_button = [[InlineKeyboardButton(text=text, url=url)]]
    else:
        progress_button = [[InlineKeyboardButton(text=text, callback_data='*')]]

    return InlineKeyboardMarkup(inline_keyboard=progress_button)
