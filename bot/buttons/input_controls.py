from aiogram.types import InlineKeyboardButton

# Кнопки для управления мышью
mouse_left = InlineKeyboardButton(text='Левый клик', callback_data='mouse_left')
mouse_right = InlineKeyboardButton(text='Правый клик', callback_data='mouse_right')

# Кнопки для перемещения
up = InlineKeyboardButton(text='↑', callback_data='move_up')
down = InlineKeyboardButton(text='↓', callback_data='move_down')
left = InlineKeyboardButton(text='←', callback_data='move_left')
right = InlineKeyboardButton(text='→', callback_data='move_right')

# Кнопки для клавиатуры
space = InlineKeyboardButton(text='Пробел', callback_data='press_space')
backspace = InlineKeyboardButton(text='Backspace', callback_data='press_backspace')
enter = InlineKeyboardButton(text='Enter', callback_data='press_enter')

# Дополнительные кнопки
replace_mouse = InlineKeyboardButton(text='Переключить на мышь', callback_data='replace_mouse')

# Кнопка для сворачивания всех окон
minimize = InlineKeyboardButton(text='Свернуть все окна', callback_data='minimize')
