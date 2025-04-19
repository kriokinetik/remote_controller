from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
import pyautogui

import tools
from bot.filters import BotAccessFilter
from tools.logger import logger_event_info
from config import SCREENSHOT_NAME

router = Router()


# Обработчик для кнопок мыши
@router.callback_query(F.data.in_({"mouse_right", "mouse_left"}))
async def mouse_button_click_handler(callback: CallbackQuery):
    logger_event_info(callback)

    buttons = {
        "right": "Right",
        "left": "Left"
    }

    button = callback.data.split("_")[1]

    pyautogui.click(button=button)
    await callback.answer(f"🖱️ {buttons[button]}-click pressed")


# Обработчик для стрелок
@router.callback_query(F.data.in_({"move_right", "move_left", "move_up", "move_down"}))
async def arrows_click_handler(callback: CallbackQuery):
    logger_event_info(callback)

    arrows = {
        "right": "→ Right",
        "left": "← Left",
        "up": "↑ Up",
        "down": "↓ Down"
    }

    arrow = callback.data.split("_")[1]

    pyautogui.press(arrow)
    await callback.answer(f"{arrows[arrow]} key pressed")


# Обработчик для кнопок Space, Backspace, Enter
@router.callback_query(F.data.in_({"press_space", "press_backspace", "press_enter"}))
async def buttons_click_handler(callback: CallbackQuery):
    logger_event_info(callback)

    button = callback.data.split("_")[1]

    pyautogui.press(button)
    await callback.answer(f"🕹️'{button}' key pressed")


# Обработчик для кнопки "Свернуть все окна"
@router.message(Command("minimize"), BotAccessFilter())
async def minimize_windows_handler(message: Message):
    logger_event_info(message)

    pyautogui.hotkey("win", "d")

    with tools.screenshot.overlay_cursor_on_screenshot(True) as image:
        image.seek(0)
        await message.reply_document(
            caption="📍 Windows successfully minimized/restored",
            document=BufferedInputFile(file=image.read(), filename=SCREENSHOT_NAME)
        )


@router.message(Command("help_cursor"), BotAccessFilter())
async def help_cursor_handler(message: Message):
    logger_event_info(message)

    bound_x, bound_y = pyautogui.size()

    await message.answer(
        f"📍 To move the cursor, just send a message with coordinates, "
        f"following the format and limits below:\n\n"
        f"↔️ x: <code>1 — {bound_x - 1}</code>\n"
        f"↕️ y: <code>1 — {bound_y - 1}</code>\n\n"
        f"Format: <code>x y</code>\n"
    )


# Обработчик для получения координат мыши
@router.message(F.text.regexp(r"^\d+\s\d+$"), BotAccessFilter())
async def move_cursor_handler(message: Message):
    logger_event_info(message)

    x, y = map(int, message.text.split())
    bound_x, bound_y = pyautogui.size()
    if 1 <= x < bound_x and 1 <= y < bound_y:
        pyautogui.moveTo(x, y)
        with tools.screenshot.overlay_cursor_on_screenshot(True) as image:
            image.seek(0)
            await message.reply_document(
                caption=f"📍 Cursor moved to ({x}, {y})",
                document=BufferedInputFile(file=image.read(), filename=SCREENSHOT_NAME)
            )
    else:
        await message.reply("❌ Coordinates out of range")
