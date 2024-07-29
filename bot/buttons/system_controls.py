from aiogram.types import InlineKeyboardButton

# Кнопки подтверждения выключения компьютера
shutdown_confirmation_buttons = [
    InlineKeyboardButton(text='Подтвердить', callback_data='confirm_shutdown'),
    InlineKeyboardButton(text='Отменить', callback_data='cancel_shutdown')
]

# Кнопки подтверждения перезагрузки компьютера
restart_confirmation_buttons = [
    InlineKeyboardButton(text='Подтвердить', callback_data='confirm_restart'),
    InlineKeyboardButton(text='Отменить', callback_data='cancel_restart')
]
