from aiogram.types import InlineKeyboardButton

# Кнопка для открытия клавиатуры и мыши
input_controls = InlineKeyboardButton(text="Mouse & Keyboard", callback_data="input_controls")

# Кнопка "Домой"
main_button = InlineKeyboardButton(text="🏠 Home", callback_data="main")

# Кнопка для получения скриншота
screenshot = InlineKeyboardButton(text="Screenshot", callback_data="screenshot")

# Кнопка для измерения скорости интернета
speed_test = InlineKeyboardButton(text="Internet Speed Test", callback_data="speed_test")
