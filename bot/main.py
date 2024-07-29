import asyncio
import sys
import logging
from aiogram import Bot, Dispatcher, exceptions, types
from aiogram.client.default import DefaultBotProperties
from aiogram.methods import DeleteWebhook
from aiogram.types import BotCommand
from aiogram.enums import ParseMode

import handlers
from config_reader import token, LOG_FILE

# Создание собственного логгера
logger = logging.getLogger('remote_controller')


def logger_info(event: types.Message | types.CallbackQuery):
    username = event.from_user.username
    user_id = event.from_user.id
    if isinstance(event, types.Message):
        content = event.text
        logger.info(f'Received message from @{username} id={user_id} — "{content}"')
    else:
        content = event.data
        logger.info(f'Received callback from @{username} id={user_id} — "{content}"')


def logger_error(exception, exc_info=False):
    logger.error(str(exception), exc_info=exc_info)


async def main():
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(bot=bot)
    await bot.set_my_commands([
        BotCommand(command='restart', description='Перезагрузить ПК'),
        BotCommand(command='shutdown', description='Выключить ПК'),
    ])
    dp.include_routers(handlers.main_window.router, handlers.subhandlers.input_controls.router,
                       handlers.subhandlers.retrieve_file.router, handlers.subhandlers.system_controls.router)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    file_handler = logging.FileHandler(filename=LOG_FILE, mode='w', encoding='utf-8')
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S',
                        level=logging.INFO,
                        handlers=[file_handler, stream_handler]
                        )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Program interrupted by the user')
    except exceptions.TelegramNetworkError as e:
        logger.critical(str(e) + '__name__')
    except exceptions.TelegramBadRequest as e:
        logger.error(str(e) + '__name__')
