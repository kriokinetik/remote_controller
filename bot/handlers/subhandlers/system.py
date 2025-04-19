from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import os
import ctypes

from bot import keyboards
from bot.filters import BotAccessFilter
from tools.logger import logger_event_info

router = Router()


@router.message(Command("lock"), BotAccessFilter())
async def minimize_windows_handler(message: Message):
    logger_event_info(message)

    ctypes.windll.user32.LockWorkStation()
    await message.answer("🔒 Computer locked")


# Обработчик для запроса подтверждения перезагрузки или выключения компьютера
@router.message(Command("restart", "shutdown"), BotAccessFilter())
async def system_control_handler(message: Message):
    logger_event_info(message)

    action = message.text.lower()
    confirmation_keyboard = None

    match action:
        case "/restart":
            confirmation_keyboard = keyboards.system.restart_confirmation
        case "/shutdown":
            confirmation_keyboard = keyboards.system.shutdown_confirmation

    await message.reply("❗ Are you sure?", reply_markup=confirmation_keyboard)


# Обработчик для отмены запроса перезагрузки или выключения
@router.callback_query(F.data.in_({"cancel_restart", "cancel_shutdown"}))
async def cancel_system_control_handler(callback: CallbackQuery):
    logger_event_info(callback)
    await callback.message.edit_text("❌ Canceled.")


# Обработчик подтверждения перезагрузки или выключения
@router.callback_query(F.data.in_({"confirm_restart", "confirm_shutdown"}))
async def confirm_system_control_handler(callback: CallbackQuery):
    logger_event_info(callback)

    match callback.data:
        case "confirm_restart":
            await callback.message.edit_text("💻 The computer is restarting.")
            os.system("shutdown -r -t 0")  # Перезагрузка компьютера
        case "confirm_shutdown":
            await callback.message.edit_text("💻 The computer is shutting down.")
            os.system("shutdown /p /f")  # Выключение компьютера
