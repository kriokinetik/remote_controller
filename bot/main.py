import asyncio
import threading
import sys
import ctypes
from PIL import Image
from pystray import Icon, Menu, MenuItem
import logging
from aiogram import Bot, Dispatcher, exceptions, types
from aiogram.client.default import DefaultBotProperties
from aiogram.methods import DeleteWebhook
from aiogram.types import BotCommand
from aiogram.enums import ParseMode

import handlers
from config_reader import token, LOG_FILE

# Глобальная переменная для отслеживания состояния окна
console_hidden = False

# Функция скрытия консольного окна (только для Windows)
def hide_console():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd:
        ctypes.windll.user32.ShowWindow(whnd, 0)  # SW_HIDE = 0

# Функция показа консольного окна
def show_console():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd:
        ctypes.windll.user32.ShowWindow(whnd, 5)  # SW_SHOW = 5

# Функция переключения видимости консольного окна
def toggle_console():
    global console_hidden
    if console_hidden:
        show_console()
    else:
        hide_console()
    console_hidden = not console_hidden

# Настройка логирования
logger = logging.getLogger('remote_controller')

def logger_info(event: types.Message | types.CallbackQuery):
    username = event.from_user.username
    user_id = event.from_user.id
    content = event.text if isinstance(event, types.Message) else event.data
    logger.info(f'Received event from @{username} id={user_id} — "{content}"')

def logger_error(exception, exc_info=False):
    logger.error(str(exception), exc_info=exc_info)

# Основная асинхронная функция запуска бота
async def start_bot():
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

# Функция запуска бота в отдельном потоке
def run_bot():
    asyncio.run(start_bot())

# Функция выхода из трея
def exit_action(icon, item):
    logger.info('Exiting from tray')
    icon.stop()
    sys.exit()

# Функция для показа/сокрытия окна консоли из трея
def toggle_window(icon, item):
    toggle_console()

# Функция создания иконки в трее
def run_tray():
    hide_console()  # Скрываем консольное окно при запуске

    image = Image.open("icon.png")  # Иконка для трея (16x16)
    menu = Menu(
        MenuItem('Show/Hide Console', toggle_window),  # Пункт для показа/сокрытия консоли
        MenuItem('Quit', exit_action)  # Пункт для выхода
    )
    icon = Icon("remote_controller", image, "remote_controller", menu)

    # Запуск бота в фоне
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Запуск иконки в трее
    icon.run()

if __name__ == '__main__':
    file_handler = logging.FileHandler(filename=LOG_FILE, mode='w', encoding='utf-8')
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S',
                        level=logging.INFO,
                        handlers=[file_handler, stream_handler]
                        )
    try:
        run_tray()
    except KeyboardInterrupt:
        logger.info('Program interrupted by the user')
    except exceptions.TelegramNetworkError as e:
        logger.critical(str(e))
    except exceptions.TelegramBadRequest as e:
        logger.error(str(e))
