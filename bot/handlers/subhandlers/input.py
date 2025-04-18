from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
import pyautogui

import tools
from tools.logger import logger_event_info
from bot.states import DataStates
from bot import keyboards
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
@router.callback_query(F.data == "minimize")
async def minimize_windows_handler(callback: CallbackQuery):
    logger_event_info(callback)

    pyautogui.hotkey("win", "d")
    await callback.answer("Windows successfully minimized")


# Обработчик для запроса координат мыши
@router.callback_query(F.data == "replace_mouse")
async def request_coordinates_handler(callback: CallbackQuery, state: FSMContext):
    logger_event_info(callback)

    bound_x, bound_y = pyautogui.size()
    await callback.message.edit_text(
        text=f"📍 Enter cursor coordinates\n"
             f"↔️ <code>X: 0 — {bound_x - 1}</code>\n"
             f"↕️ <code>Y: 0 — {bound_y - 1}</code>\n\n"
             f"<i>Send coordinates in format:</i> <code>x y</code>\n",
        reply_markup=keyboards.input.to_input_controls
    )
    await state.set_state(DataStates.coordinates)


# Обработчик для получения координат мыши
@router.message(DataStates.coordinates)
async def replace_mouse_handler(message: Message):
    logger_event_info(message)

    try:
        x, y = map(int, message.text.split())
        bound_x, bound_y = pyautogui.size()
        if 0 <= x < bound_x and 0 <= y < bound_y:
            pyautogui.moveTo(x, y)
            with tools.screenshot.overlay_cursor_on_screenshot(True) as image:
                image.seek(0)
                await message.answer_document(
                    caption=f"📍 Cursor moved to ({x}, {y})",
                    document=BufferedInputFile(file=image.read(), filename=SCREENSHOT_NAME)
                )
        else:
            await message.reply("❌ Coordinates out of range")
    except (ValueError, IndexError):
        await message.reply("❌ Incorrect coordinate format")
