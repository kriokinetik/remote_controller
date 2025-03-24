from aiogram.types import InlineKeyboardMarkup
from bot import buttons

restart_confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        buttons.system_controls.restart_confirmation_buttons
    ]
)

shutdown_confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        buttons.system_controls.shutdown_confirmation_buttons
    ]
)
