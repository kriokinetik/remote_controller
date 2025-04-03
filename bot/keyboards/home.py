from aiogram.types import InlineKeyboardMarkup
from bot import buttons


main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.home.input_controls],
        [buttons.home.screenshot],
        [buttons.home.speed_test]
    ]
)
