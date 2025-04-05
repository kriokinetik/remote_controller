import asyncio
from PyQt6.QtCore import QThread, pyqtSignal
from bot import TelegramBot
from config import get_config


class BotThread(QThread):
    log_signal = pyqtSignal(str)
    stop_signal = pyqtSignal()  # Сигнал для остановки потока

    def __init__(self):
        super().__init__()
        self.bot = TelegramBot(get_config()["token"])  # Создаем экземпляр бота
        self.loop = asyncio.new_event_loop()  # Создаем новый цикл событий для потока
        self.bot_loop_task = None

    def run(self):
        asyncio.set_event_loop(self.loop)

        if self.bot.token != get_config()["token"]:
            self.bot.set_token(get_config()["token"])

        try:
            self.bot_loop_task = self.loop.create_task(self.bot.run())
            self.loop.run_until_complete(self.bot_loop_task)
        except Exception as e:
            self.log_signal.emit(f"Error in bot: {str(e)}")
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())

    def stop(self):
        """Асинхронно останавливает бота и завершает поток."""
        if self.bot:
            async def _shutdown():
                await self.bot.stop()

            if self.loop.is_running():
                asyncio.run_coroutine_threadsafe(_shutdown(), self.loop)
            else:
                # Теоретически не должно быть такого состояния
                self.log_signal.emit("Loop is not running during stop")
