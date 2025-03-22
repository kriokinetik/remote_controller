from aiogram.types import InlineKeyboardMarkup
import buttons  # Импорт кнопок из модуля buttons

# Создание главной клавиатуры
main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.main_window.input_controls],  # Клавиатура и мышь
        [buttons.main_window.retrieve_file],  # Получение файла
        [buttons.main_window.screenshot],  # Скриншот
        [buttons.main_window.speed_test]  # Скорость интернета
    ]
)


