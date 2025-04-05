from aiogram.types import Message
from aiogram.filters import Filter

from config import get_config


class BotAccessFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        """
        Проверяет, является ли отправитель сообщения администратором бота.
        """
        admin = get_config()["admin"]

        return message.from_user.id in admin
