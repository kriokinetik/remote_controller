import asyncio
from PyQt6.QtCore import QThread, pyqtSignal
from aiogram.utils.token import TokenValidationError

from bot import TelegramBot


class BotThread(QThread):
    log_signal = pyqtSignal(str)
    stop_signal = pyqtSignal()  # Сигнал для остановки потока

    def __init__(self):
        super().__init__()
        self.bot = None
        self._running = False
        self.set_bot()
        self.loop = asyncio.new_event_loop()
        self.bot_loop_task = None

    def is_bot_running(self):
        if self.bot is None:
            return False

        return self.bot.is_running()

    def set_bot(self):
        try:
            self.bot = TelegramBot()
        except TokenValidationError:
            self.bot = None

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.start_bot()

    def start_bot(self):
        if self.is_bot_running():
            return

        if self.bot is None:
            self.set_bot()

        try:
            self.bot_loop_task = self.loop.create_task(self.bot.run())
            self.loop.run_until_complete(self.bot_loop_task)
        except TokenValidationError:
            self.log_signal.emit("<font color='red'>Invalid token! Please enter a valid token and restart the bot.</font>")
        except Exception as e:
            self.log_signal.emit(f"Error in bot: {e}")
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())

    def stop_bot(self):
        """Асинхронно останавливает бота и завершает поток."""
        if self.bot:
            async def _shutdown():
                await self.bot.stop()

            if self.bot.is_running():
                if self.loop.is_running():
                    asyncio.run_coroutine_threadsafe(_shutdown(), self.loop)
                else:
                    # Теоретически не должно быть такого состояния
                    self.log_signal.emit("Loop is not running during stop")
