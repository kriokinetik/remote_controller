import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile

import tools
from tools.logger import logger_event_info, logger_error
from bot import keyboards
from bot.states import DataStates
from bot.handlers.subhandlers.files import navigate_to_path
from bot.filters import BotAccessFilter
from config import SCREENSHOT_NAME, PAGE_SIZE

router = Router()


# Обработчик команды /start
@router.message(Command("start"), BotAccessFilter())
async def send_remote_controller_handler(message: Message):
    logger_event_info(message)

    await message.answer(text="remote controller", reply_markup=keyboards.home.main_keyboard)


# Обработчик для запроса на отправку скриншота
@router.callback_query(F.data == "screenshot")
async def send_screenshot_handler(callback: CallbackQuery):
    logger_event_info(callback)

    with tools.screenshot.overlay_cursor_on_screenshot(False) as image:
        image.seek(0)
        await callback.message.answer_document(document=BufferedInputFile(file=image.read(),
                                                                          filename=SCREENSHOT_NAME),
                                               caption="🖼 Screenshot captured",
                                               disable_content_type_detection=True)

    await callback.answer()


# Обработчик для запроса на отправку пульта управления клавиатурой и мышью
@router.callback_query(F.data == "input_controls")
async def send_input_controls_handler(callback: CallbackQuery, state: FSMContext):
    logger_event_info(callback)

    await callback.message.edit_text(text="Клавиатура и мышь", reply_markup=keyboards.input.input_controls)
    await callback.answer("")
    await callback.message.edit_text(text=f"Mouse & Keyboard",
    if await state.get_state() is not None:
        await state.set_state(state=None)


# Обработчик для запроса на отправку главного окна
@router.callback_query(F.data == "main")
async def send_main_window_handler(callback: CallbackQuery, state: FSMContext):
    logger_event_info(callback)

    await callback.message.edit_text(text="remote controller", reply_markup=keyboards.home.main_keyboard)
    await callback.answer("")
    if await state.get_state() is not None:
        await state.set_state(state=None)


# Обработчик для отправки меню проводника
@router.callback_query(F.data == "retrieve_file")
async def retrieve_file_menu_handler(callback: CallbackQuery, state: FSMContext):
    logger_event_info(callback)

    desktop_path = tools.file_ops.get_desktop_path()
    await navigate_to_path(callback, state, desktop_path)

    # Установка состояния ожидания сообщения с путем к файлу
    await state.set_state(DataStates.path)

    await callback.answer()


async def run_speedtest(message: Message):
    try:
        download, upload = await tools.speedtest.speed_test()
        await message.edit_text(f"🌐 Internet Speed Test Results\n\n"
                                f"⬇️ <code>Download: {download}ps</code>\n"
                                f"⬆️ <code>Upload: {upload}ps</code>")
    except Exception as e:
        await message.edit_text(f"❌ Speed test failed: {e}")
        logger_error(e, exc_info=True)

# Обработчик для измерения скорости интернета
@router.callback_query(F.data == "speed_test")
async def send_speed_test_handler(callback: CallbackQuery):
    logger_event_info(callback)

    message = await callback.message.answer("🔄 Running Internet Speed Test...")
    await callback.answer()

    asyncio.create_task(run_speedtest(message))

    await callback.answer("Uploading...")
