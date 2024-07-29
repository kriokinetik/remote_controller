from aiogram.types import InlineKeyboardButton

# Кнопка для перехода в родительский каталог
parent_directory = InlineKeyboardButton(text='⬅', callback_data='traverse_up_directory')

# Кнопка для перехода на диск C:
disk_C = InlineKeyboardButton(text='C:', callback_data='C:\\')

# Кнопка для перехода на диск D:
disk_D = InlineKeyboardButton(text='D:', callback_data='D:\\')
