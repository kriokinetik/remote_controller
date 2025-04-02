from aiogram.types import InlineKeyboardMarkup
from bot import buttons


restart_confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        buttons.system.restart_confirmation_buttons
    ]
)

shutdown_confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        buttons.system.shutdown_confirmation_buttons
    ]
)
