from aiogram.types import InlineKeyboardMarkup
import buttons  # Импорт кнопок из модуля buttons

# Создание клавиатуры для управления клавиатурой и мышью
input_controls = InlineKeyboardMarkup(
    inline_keyboard=[
        # Кнопки для управления мышью
        [buttons.input_controls.mouse_left, buttons.input_controls.up, buttons.input_controls.mouse_right],
        # Кнопки для управления клавиатурой
        [buttons.input_controls.left, buttons.input_controls.down, buttons.input_controls.right],
        [buttons.input_controls.space, buttons.input_controls.backspace, buttons.input_controls.enter],
        # Кнопки пробела, backspace и enter
        [buttons.input_controls.replace_mouse],  # Кнопка для замены режима управления мышью
        [buttons.input_controls.minimize],  # Кнопка для сворачивания всех окон
        [buttons.main_window.main_button]  # Кнопка для возврата к главному меню
    ]
)

to_input_controls = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.main_window.input_controls]
    ]
)
