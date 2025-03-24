import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.methods import DeleteWebhook
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from bot import handlers
from config_reader import token


async def run_bot():
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(bot=bot)

    await bot.set_my_commands([
        BotCommand(command='restart', description='Перезагрузить ПК'),
        BotCommand(command='shutdown', description='Выключить ПК'),
    ])

    dp.include_routers(
        handlers.main_window.router, handlers.subhandlers.input_controls.router,
        handlers.subhandlers.retrieve_file.router, handlers.subhandlers.system_controls.router
    )

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

def start_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())