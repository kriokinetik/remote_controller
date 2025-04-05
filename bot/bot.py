from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.methods import DeleteWebhook
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.utils.token import TokenValidationError

from bot import handlers
from tools import logger


class TelegramBot:
    def __init__(self, token):
        self.token = token
        self._running = False

        try:
            self.bot = Bot(token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
            self.dp = Dispatcher(bot=self.bot)
            self.include_routers()
        except TokenValidationError:
            logger.logger_error("Token is invalid!")
            return

    def set_token(self, token):
        self.token = token
        self.bot = Bot(token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher(bot=self.bot)
        self.include_routers()

    async def set_commands(self):
        await self.bot.set_my_commands(
            [
                BotCommand(command="cd", description="Navigate to a specified directory"),
                BotCommand(command="sendfile", description="Send a file"),
                BotCommand(command="remote", description="Send the control panel to manage the device"),
                BotCommand(command="screenshot", description="Capture and send a screenshot"),
                BotCommand(command="speedtest", description="Measure and send internet speed"),
                BotCommand(command="restart", description="Restart the computer"),
                BotCommand(command="shutdown", description="Shutdown the computer"),
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
        if self._running:
            return

        self._running = True

        try:
            await self.set_commands()
            await self.bot(DeleteWebhook(drop_pending_updates=True))
            await self.dp.start_polling(self.bot)
        except Exception as e:
            print(f"[Aiogram error] {e}")

    async def stop(self):
        self._running = False
        try:
            await self.dp.stop_polling()  # Завершаем polling
        except Exception as e:
            print(e)
