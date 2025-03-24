from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import os

from bot import keyboards
from bot.filters import BotAccessFilter
from bot.logger import logger_event_info

router = Router()


# Обработчик для запроса подтверждения перезагрузки или выключения компьютера
@router.message(Command('restart', 'shutdown'), BotAccessFilter())
async def system_control_handler(message: Message):
    logger_event_info(message)

    # Определяем, какое действие требуется (перезагрузка или выключение)
    action = message.text.lower()
    confirmation_keyboard = None

    if action == '/restart':
        confirmation_keyboard = keyboards.system_controls.restart_confirmation
    elif action == '/shutdown':
        confirmation_keyboard = keyboards.system_controls.shutdown_confirmation

    # Отправляем запрос на подтверждение с клавиатурой для пользователя
    await message.reply(text='Вы уверены?', reply_markup=confirmation_keyboard)


# Обработчик для отмены запроса перезагрузки или выключения
@router.callback_query(F.data.in_({'cancel_restart', 'cancel_shutdown'}))
async def cancel_system_control_handler(callback: CallbackQuery):
    logger_event_info(callback)

    # Отменяем операцию и сообщаем об этом пользователю
    await callback.message.edit_text(text='Отменено.')


# Обработчик подтверждения перезагрузки или выключения
@router.callback_query(F.data.in_({'confirm_restart', 'confirm_shutdown'}))
async def confirm_system_control_handler(callback: CallbackQuery):
    logger_event_info(callback)

    # В зависимости от выбора пользователя, выполняем перезагрузку или выключение
    if callback.data == 'confirm_restart':
        await callback.message.edit_text('Компьютер перезагружается.')
        os.system('shutdown -r -t 0')  # Перезагрузка компьютера
    elif callback.data == 'confirm_shutdown':
        await callback.message.edit_text('Компьютер выключается.')
        os.system('shutdown /p /f')  # Выключение компьютера
