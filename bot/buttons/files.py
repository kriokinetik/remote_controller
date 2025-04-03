from aiogram.types import InlineKeyboardButton


show_files = InlineKeyboardButton(text="🔖 Show Files", callback_data="show_file")
show_folders = InlineKeyboardButton(text="📁 Show Folders", callback_data="show_folder")

prev_page = InlineKeyboardButton(text="◀", callback_data="prev_page")
next_page = InlineKeyboardButton(text="▶", callback_data="next_page")
