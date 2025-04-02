from aiogram.types import InlineKeyboardButton

# Кнопки подтверждения выключения компьютера
shutdown_confirmation_buttons = [
    InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_shutdown"),
    InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_shutdown")
]

# Кнопки подтверждения перезагрузки компьютера
restart_confirmation_buttons = [
    InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_restart"),
    InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_restart")
]
