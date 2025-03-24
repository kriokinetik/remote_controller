from aiogram.types import InlineKeyboardButton

# Кнопка для открытия клавиатуры и мыши
input_controls = InlineKeyboardButton(text="Клавиатура и мышь", callback_data="input_controls")

# # Кнопка для открытия управления играми
# game_controls = InlineKeyboardButton(text='Управление играми', callback_data='game_controls')

# Кнопка "Домой"
main_button = InlineKeyboardButton(text="На главную", callback_data="main")

# Кнопка для получения скриншота
screenshot = InlineKeyboardButton(text="Скриншот", callback_data="screenshot")

# Кнопка для управления файлами
retrieve_file = InlineKeyboardButton(text="Управление файлами", callback_data="retrieve_file")

# Кнопка для измерения скорости интернета
speed_test = InlineKeyboardButton(text="Speed Test", callback_data="speed_test")
