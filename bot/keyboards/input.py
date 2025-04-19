from aiogram.types import InlineKeyboardMarkup
from bot import buttons


input_controls = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.input.mouse_left, buttons.input.up, buttons.input.mouse_right],
        [buttons.input.left, buttons.input.down, buttons.input.right],
        [buttons.input.space, buttons.input.backspace, buttons.input.enter]
    ]
)
