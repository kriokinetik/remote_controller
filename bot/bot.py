from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.methods import DeleteWebhook
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.utils.token import TokenValidationError

from bot import handlers
from tools import logger
from config import get_config


class TelegramBot:
    def __init__(self):
        self.token = get_config().get("token", "")
        self.bot = None
        self.dp = None
        self._is_token_valid = False
        self._running = False
        self._routers_included = False

        self.create_bot()

    def is_running(self):
        return self._running

    def is_token_valid(self):
        return self._is_token_valid

    def create_bot(self):
        try:
            self.bot = Bot(token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
            self._is_token_valid = True
            self.dp = Dispatcher(bot=self.bot)
            self.include_routers()
        except TokenValidationError:
            self._is_token_valid = False
            logger.logger_error("Token is invalid!")

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
        if self._routers_included:
            return

        self.dp.include_routers(
            handlers.home.router,
            handlers.subhandlers.input.router,
            handlers.subhandlers.files.router,
            handlers.subhandlers.system.router
        )

        self._routers_included = True

    async def run(self):
        if self.is_running():
            return

        if self.bot is None:
            token = get_config().get("token", "")

            if self.token != token:
                self.token = token
                self.create_bot()

        if not self.is_token_valid():
            raise TokenValidationError

        try:
            await self.set_commands()
            await self.bot(DeleteWebhook(drop_pending_updates=True))
            self._running = True
            await self.dp.start_polling(self.bot)
        except Exception as e:
            print(f"[Aiogram error] {e}")

    async def stop(self):
        if not self.is_token_valid():
            return

        if self.is_running():
            try:
                await self.dp.stop_polling()  # Завершаем polling
                self._running = False
            except Exception as e:
                print(e)
