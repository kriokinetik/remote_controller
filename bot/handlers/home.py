import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile

import tools
from tools.logger import logger_event_info, logger_error
from bot import keyboards
from bot.filters import BotAccessFilter
from config import SCREENSHOT_NAME

router = Router()


@router.message(Command("start"), BotAccessFilter())
async def start_handler(message: Message):
    logger_event_info(message)

    await message.answer(
        "This bot lets you control your PC remotely via Telegram.\n"
        "Use /help to see all available commands."
    )


@router.message(Command("screenshot"), BotAccessFilter())
async def screenshot_handler(message: Message):
    logger_event_info(message)

    with tools.screenshot.overlay_cursor_on_screenshot(False) as image:
        image.seek(0)
        await message.answer_document(
            document=BufferedInputFile(file=image.read(), filename=SCREENSHOT_NAME),
            caption="🖼 Screenshot captured",
            disable_content_type_detection=True
        )


@router.message(Command("remote"), BotAccessFilter())
async def remote_handler(message: Message, state: FSMContext):
    logger_event_info(message)

    await message.answer(text="Mouse & Keyboard",
                         reply_markup=keyboards.input.input_controls)

    if await state.get_state() is not None:
        await state.set_state(state=None)


@router.callback_query(F.data == "remote")
async def callback_remote_handler(callback: CallbackQuery, state: FSMContext):
    logger_event_info(callback)

    await callback.message.edit_text(text="Mouse & Keyboard",
                                     reply_markup=keyboards.input.input_controls)
    await callback.answer()
    if await state.get_state() is not None:
        await state.set_state(state=None)


async def run_speedtest(message: Message):
    try:
        download, upload = await tools.speedtest.speed_test()
        await message.edit_text(
            f"🌐 Internet Speed Test Results\n\n"
            f"⬇️ <code>Download: {download}ps</code>\n"
            f"⬆️ <code>Upload: {upload}ps</code>"
        )
    except Exception as e:
        await message.edit_text(f"❌ Speed test failed: {e}")
        logger_error(e, exc_info=True)


@router.message(Command("speedtest"), BotAccessFilter())
async def speedtest_handler(message: Message):
    logger_event_info(message)

    message = await message.answer("🔄 Running Internet Speed Test...")
    asyncio.create_task(run_speedtest(message))


@router.callback_query(F.data == "*")
async def empty_handler(callback: CallbackQuery):
    logger_event_info(callback)

    await callback.answer("Uploading...")
