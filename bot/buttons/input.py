from aiogram.types import InlineKeyboardButton

# Кнопки для управления мышью
mouse_left = InlineKeyboardButton(text="Left Click", callback_data="mouse_left")
mouse_right = InlineKeyboardButton(text="Right Click", callback_data="mouse_right")

# Кнопки для перемещения
up = InlineKeyboardButton(text="↑", callback_data="move_up")
down = InlineKeyboardButton(text="↓", callback_data="move_down")
left = InlineKeyboardButton(text="←", callback_data="move_left")
right = InlineKeyboardButton(text="→", callback_data="move_right")

# Кнопки для клавиатуры
space = InlineKeyboardButton(text="Space", callback_data="press_space")
backspace = InlineKeyboardButton(text="Backspace", callback_data="press_backspace")
enter = InlineKeyboardButton(text="Enter", callback_data="press_enter")

# Кнопки для регулировки громкости
volume_down = InlineKeyboardButton(text="🔉", callback_data="volumedown")
volume_up = InlineKeyboardButton(text="🔊", callback_data="volumeup")
volume_mute = InlineKeyboardButton(text="🔇", callback_data="volumemute")
