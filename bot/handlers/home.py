from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile

import tools
from tools.logger import logger_event_info
from bot import keyboards, states
from bot.filters import BotAccessFilter
from config import SCREENSHOT_NAME

router = Router()


# Обработчик команды /start
@router.message(Command("start"), BotAccessFilter())
async def send_remote_controller_handler(message: Message):
    logger_event_info(message)

    # Отправка клавиатуры пользователю
    await message.answer(text="remote controller", reply_markup=keyboards.home.main_keyboard)


# Обработчик для запроса на отправку скриншота
@router.callback_query(F.data == "screenshot")
async def send_screenshot_handler(callback: CallbackQuery):
    logger_event_info(callback)

    with tools.screenshot.overlay_cursor_on_screenshot(False) as image:
        image.seek(0)
        await callback.message.answer_document(document=BufferedInputFile(file=image.read(),
                                                                          filename=SCREENSHOT_NAME))

    await callback.answer("Снимок экрана сделан")


# Обработчик для запроса на отправку пульта управления клавиатурой и мышью
@router.callback_query(F.data == "input_controls")
async def send_input_controls_handler(callback: CallbackQuery, state: FSMContext):
    logger_event_info(callback)

    await callback.message.edit_text(text="Клавиатура и мышь", reply_markup=keyboards.input.input_controls)
    await callback.answer("")
    if await state.get_state() is not None:
        await state.set_state(state=None)


# Обработчик для запроса на отправку главного окна
@router.callback_query(F.data == "main")
async def send_main_window_handler(callback: CallbackQuery, state: FSMContext):
    logger_event_info(callback)

    await callback.message.edit_text(text="remote controller", reply_markup=keyboards.home.main_keyboard)
    await callback.answer("")
    if await state.get_state() is not None:
        await state.set_state(state=None)


# # Обработчик для запроса на отправку пульта управления играми
# @router.callback_query(F.data == 'game_controls')
# async def games_control_handler(callback: CallbackQuery):
#     await callback.message.edit_text(text='Управление играми', reply_markup=keyboards.game_controls.game_controls)
#     await callback.answer('')


# Обработчик для отправки меню проводника
@router.callback_query(F.data == "retrieve_file")
async def retrieve_file_menu_handler(callback: CallbackQuery, state: FSMContext):
    logger_event_info(callback)

    # Получение пути к рабочему столу и обновление данных в состоянии
    data = await state.update_data(path=tools.file_ops.get_desktop_path())

    # Формирование клавиатуры и сообщения с файлами и папками
    files, folders = tools.file_ops.get_directory_info(current_directory=data["path"])
    await callback.message.edit_text(text=files, reply_markup=keyboards.files.next_directory(folders))

    # Установка состояния ожидания сообщения с путем к файлу
    await state.set_state(states.DataStates.path)

    # Отправка ответа пользователю
    await callback.answer("")


# Обработчик для измерения скорости интернета
@router.callback_query(F.data == "speed_test")
async def send_speed_test_handler(callback: CallbackQuery):
    logger_event_info(callback)

    # Получение пути к рабочему столу и обновление данных в состоянии
    msg = await callback.message.answer(text="Speedtest запущен...")
    # Отправка ответа пользователю
    await callback.answer("")

    download, upload = tools.speedtest.speed_test()

    await msg.edit_text(text=f"Download: {download}\n"
                             f"Upload: {upload}"
                        )
