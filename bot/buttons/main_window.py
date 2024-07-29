from aiogram.types import InlineKeyboardButton

# Кнопка для открытия клавиатуры и мыши
input_controls = InlineKeyboardButton(text='Клавиатура и мышь', callback_data='input_controls')

# # Кнопка для открытия управления играми
# game_controls = InlineKeyboardButton(text='Управление играми', callback_data='game_controls')

# Кнопка "Домой"
main_button = InlineKeyboardButton(text='На главную', callback_data='main')

# Кнопка для получения скриншота
screenshot = InlineKeyboardButton(text='Скриншот', callback_data='screenshot')

# Кнопка для управления файлами
retrieve_file = InlineKeyboardButton(text='Управление файлами', callback_data='retrieve_file')

# # Кнопка для выключения компьютера с подтверждением действия
# shutdown_pc = InlineKeyboardButton(text='Выключить компьютер', callback_data='shutdown_pc')
#
# # Кнопка для перезагрузки компьютера с подтверждением действия
# restart_pc = InlineKeyboardButton(text='Перезагрузить компьютер', callback_data='restart_pc')
