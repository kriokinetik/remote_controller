from aiogram.types import Message
from aiogram.filters import Filter

from config_reader import admin


class BotAccessFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        """
        Проверяет, является ли отправитель сообщения администратором бота.
        """

        # Проверяем, является ли отправитель сообщения (ID) администратором бота
        return message.from_user.id == admin

