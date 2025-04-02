from aiogram.types import InlineKeyboardButton

# Кнопка для открытия клавиатуры и мыши
input_controls = InlineKeyboardButton(text="Mouse & Keyboard", callback_data="input_controls")

# # Кнопка для открытия управления играми
# game_controls = InlineKeyboardButton(text='Управление играми', callback_data='game_controls')

# Кнопка "Домой"
main_button = InlineKeyboardButton(text="🏠 Home", callback_data="main")

# Кнопка для получения скриншота
screenshot = InlineKeyboardButton(text="Screenshot", callback_data="screenshot")

# Кнопка для управления файлами
retrieve_file = InlineKeyboardButton(text="File Manager", callback_data="retrieve_file")

# Кнопка для измерения скорости интернета
speed_test = InlineKeyboardButton(text="Internet Speed Test", callback_data="speed_test")
