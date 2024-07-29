from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
import pyautogui

from main import logger_info
from states import DataStates
from config_reader import SCREENSHOT_NAME
import keyboards
import utils

router = Router()


# Обработчик для кнопки "Левый клик"
@router.callback_query(F.data == 'mouse_left')
async def mouse_left_click_handler(callback: CallbackQuery):
    logger_info(callback)

    # Имитируем нажатие левой кнопки мыши
    pyautogui.click(button='left')
    await callback.answer('Левая кнопка мыши нажата')


# Обработчик для кнопки "Правый клик"
@router.callback_query(F.data == 'mouse_right')
async def clich_right_mouse_button_handler(callback: CallbackQuery):
    logger_info(callback)

    # Имитируем нажатие правой кнопки мыши
    pyautogui.click(button='right')
    await callback.answer('Правая кнопка мыши нажата')


# Обработчик для кнопки "Вверх"
@router.callback_query(F.data == 'move_up')
async def up_click_handler(callback: CallbackQuery):
    logger_info(callback)

    # Имитируем нажатие клавиши "Вверх"
    pyautogui.press('up')
    await callback.answer('Кнопка "Вверх" нажата')


# Обработчик для кнопки "Вниз"
@router.callback_query(F.data == 'move_down')
async def down_click_handler(callback: CallbackQuery):
    logger_info(callback)

    # Имитируем нажатие клавиши "Вниз"
    pyautogui.press('down')
    await callback.answer('Кнопка "Вниз" нажата')


# Обработчик для кнопки "Влево"
@router.callback_query(F.data == 'move_left')
async def left_click_handler(callback: CallbackQuery):
    logger_info(callback)

    # Имитируем нажатие клавиши "Влево"
    pyautogui.press('left')
    await callback.answer('Кнопка "Влево" нажата')


# Обработчик для кнопки "Вправо"
@router.callback_query(F.data == 'move_right')
async def right_click_handler(callback: CallbackQuery):
    logger_info(callback)

    # Имитируем нажатие клавиши "Вправо"
    pyautogui.press('right')
    await callback.answer('Кнопка "Вправо" нажата')


# Обработчик для кнопки "Пробел"
@router.callback_query(F.data == 'press_space')
async def space_click_handler(callback: CallbackQuery):
    logger_info(callback)

    # Имитируем нажатие клавиши "Пробел"
    pyautogui.press('space')
    await callback.answer('Кнопка "Пробел" нажата')


# Обработчик для кнопки "Backspace"
@router.callback_query(F.data == 'press_backspace')
async def backspace_click_handler(callback: CallbackQuery):
    logger_info(callback)

    # Имитируем нажатие клавиши "Backspace"
    pyautogui.press('backspace')
    await callback.answer('Кнопка "Backspace" нажата')


# Обработчик для кнопки "Enter"
@router.callback_query(F.data == 'press_enter')
async def enter_click_handler(callback: CallbackQuery):
    logger_info(callback)

    # Имитируем нажатие клавиши "Enter"
    pyautogui.press('enter')
    await callback.answer('Кнопка "Enter" нажата')


# Обработчик для кнопки "Свернуть все окна"
@router.callback_query(F.data == 'minimize')
async def minimize_windows_handler(callback: CallbackQuery):
    logger_info(callback)

    # Имитируем нажатие комбинации клавиш для сворачивания всех окон
    pyautogui.hotkey('win', 'm')
    await callback.answer(text='Окна успешно свернуты')


# Обработчик для запроса координат мыши
@router.callback_query(F.data == 'replace_mouse')
async def request_coordinates_handler(callback: CallbackQuery, state: FSMContext):
    logger_info(callback)

    bound_x, bound_y = pyautogui.size()
    await callback.message.edit_text(
        text=f'Ожидание координат (x, y)\n'
             f'x ∈ [0, {bound_x - 1}]\n'
             f'y ∈ [0, {bound_y - 1}]',
        reply_markup=keyboards.input_controls.to_input_controls
    )
    await state.set_state(DataStates.coordinates)


# Обработчик для получения координат мыши
@router.message(DataStates.coordinates)
async def replace_mouse_handler(message: Message):
    logger_info(message)

    try:
        x, y = map(int, message.text.split())
        bound_x, bound_y = pyautogui.size()
        if 0 <= x < bound_x and 0 <= y < bound_y:
            pyautogui.moveTo(x, y)
            with utils.screenshot_utils.overlay_cursor_on_screenshot(True) as image:
                image.seek(0)
                await message.answer_document(
                    caption=f'Курсор мыши перемещен в ({x}, {y})',
                    document=BufferedInputFile(file=image.read(), filename=SCREENSHOT_NAME)
                )
        else:
            await message.answer('Координаты вне допустимого диапазона')
    except (ValueError, IndexError):
        await message.answer('Некорректный формат координат')
