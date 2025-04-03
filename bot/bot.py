import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.methods import DeleteWebhook
from aiogram.types import BotCommand
from aiogram.enums import ParseMode

from bot import handlers
from config import token


class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher(bot=self.bot)

    async def set_commands(self):
        await self.bot.set_my_commands(
            [
                BotCommand(command="restart", description="Restart the computer"),
                BotCommand(command="shutdown", description="Shutdown the computer"),
                BotCommand(command="cd", description="Navigate to a specified directory"),
                BotCommand(command="sendfile", description="Send a file")
            ]
        )

    def include_routers(self):
        self.dp.include_routers(
            handlers.home.router,
            handlers.subhandlers.input.router,
            handlers.subhandlers.files.router,
            handlers.subhandlers.system.router
        )

    async def run(self):
        await self.set_commands()
        self.include_routers()
        await self.bot(DeleteWebhook(drop_pending_updates=True))
        await self.dp.start_polling(self.bot)

    def async_run(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run())
