from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest
import asyncio
import os
import time

from main import logger_info, logger_error, logger
from states import DataStates
from utils import file_operations, yandex_operations, speed_test, YandexUploader
from utils.speed_test import measure_speed
from config_reader import MAX_SIZE
import keyboards

router = Router()


@router.callback_query(F.data == 'traverse_up_directory')
async def handle_traverse_up_directory(callback: CallbackQuery, state: FSMContext):
    logger_info(callback)

    try:
        # Получаем текущий путь из состояния FSM
        current_path = (await state.get_data()).get('path', '')

        if current_path in ['D:\\', 'C:\\']:
            await callback.answer()
            return

        # Получаем путь к родительской директории
        next_path = os.path.abspath(os.path.join(current_path, '..')) + os.sep
        # Обновляем путь в состоянии FSM
        await state.update_data(path=next_path)
        # Запрашиваем файлы и папки в новом пути
        files, folders = file_operations.generate_directory_info(next_path)
        # Редактируем сообщение с файлами и папками
        await callback.message.edit_text(text=files, reply_markup=keyboards.retrieve_file.next_directory(folders))
        await callback.answer()
    except TelegramBadRequest as e:
        logger_error(e, exc_info=True)
        # В случае ошибки, возвращаем сообщение с описанием ошибки
        await callback.message.answer(f'<blockquote>{e}</blockquote>')


@router.callback_query(F.data.in_({'D:\\', 'C:\\'}))
async def handle_traverse_up_to_disk(callback: CallbackQuery, state: FSMContext):
    logger_info(callback)

    try:
        # Получаем выбранный диск из данных обратного вызова
        disk = callback.data
        # Обновляем путь в состоянии FSM
        await state.update_data(path=disk)
        # Запрашиваем файлы и папки на выбранном диске
        files, folders = file_operations.generate_directory_info(disk)
        # Редактируем сообщение с файлами и папками
        await callback.message.edit_text(text=files, reply_markup=keyboards.retrieve_file.next_directory(folders))
        await callback.answer()
    except TelegramBadRequest as e:
        logger_error(e, exc_info=True)
        # В случае ошибки, возвращаем сообщение с описанием ошибки
        await callback.message.answer(f'<blockquote>{e}</blockquote>')


@router.callback_query(F.data.endswith(os.sep))
async def handle_traverse_up_directory(callback: CallbackQuery, state: FSMContext):
    logger_info(callback)

    # Получаем текущий путь из состояния FSM
    current_path = (await state.get_data()).get('path', '')
    # Обновляем путь в состоянии FSM, добавляя выбранную папку
    next_path = current_path + callback.data
    await state.update_data(path=next_path)
    try:
        # Запрашиваем файлы и папки в новом пути
        files, folders = file_operations.generate_directory_info(next_path)
        # Редактируем сообщение с файлами и папками
        await callback.message.edit_text(text=files, reply_markup=keyboards.retrieve_file.next_directory(folders))
        await callback.answer()
    except (TelegramBadRequest, PermissionError, FileNotFoundError) as e:
        await state.update_data(path=current_path)
        logger_error(e, exc_info=True)
        # В случае ошибки, возвращаем сообщение с описанием ошибки
        await callback.message.answer(f'<blockquote>{e}</blockquote>')


@router.message(DataStates.path)
async def handle_send_document(message: Message):
    logger_info(message)

    try:
        path = message.text.replace('\\', '/')
        filesize = file_operations.get_file_or_directory_size(path)

        if os.path.isfile(path):
            _, filename = path.rsplit('/', maxsplit=1)
            is_file = True
        elif os.path.isdir(path):
            await message.reply(f'Архивируется...')
            path = file_operations.compress_folder_to_zip(path)
            _, filename = path.rsplit('/', maxsplit=1)
            filesize = os.path.getsize(path)
            is_file = False
        else:
            await message.reply('Указанный путь не существует или не является доступным файлом/папкой')
            return

        if filesize < MAX_SIZE:
            await message.reply(f'Файл <code>{filename}</code> загружается...\n')
            await message.reply_document(document=FSInputFile(path=path))
        else:
            internet_speed_task = asyncio.create_task(measure_speed("upload", False))

            rounded_filesize = speed_test.humansize(filesize)

            download_message = await message.reply(f'Файл <code>{filename}</code> загружается на Яндекс.Диск...\n'
                                                   f'Размер файла: <code>{rounded_filesize}</code>\n'
                                                   f'Время ожидания: —',
                                                   reply_markup=keyboards.retrieve_file.get_progress_keyboard('...'))

            yandex_uploader = YandexUploader(path, filesize, download_message)

            if not await yandex_uploader.check_file_existence():
                try:
                    internet_speed = await internet_speed_task
                    logger.info(f'Upload speed: {internet_speed}')  # logging

                    upload_time = filesize / internet_speed
                    estimated_time = time.strftime("%H:%M:%S", time.gmtime(upload_time))

                    yandex_uploader.upload_speed = internet_speed

                except ValueError as e:
                    estimated_time = "N/A"
                    logger_error(e)

                download_message = await download_message.edit_text(f'Файл: <code>{filename}</code>\n'
                                                                    f'Размер файла: <code>{rounded_filesize}</code>\n'
                                                                    f'Время ожидания: {estimated_time}',
                                                                    reply_markup=download_message.reply_markup
                                                                    )

                yandex_uploader.message = download_message

                await yandex_uploader.upload_file_to_yandex_disk()
                logger.info(f'Start uploading file "{path}" (size: {filesize} bytes) to Yandex Disk')  # logging

            download_link = await yandex_uploader.get_yandex_link()
            logger.info(f'File "{path}" (size: {filesize} bytes) has been successfully uploaded to Yandex Disk')
            await download_message.edit_text(f'Файл: <code>{filename}</code>\n'
                                             f'Размер файла: <code>{rounded_filesize}</code>',
                                             reply_markup=keyboards.retrieve_file.get_progress_keyboard(
                                                 'Скачать файл...', download_link)
                                             )
            if not is_file:
                os.remove(path)

    except (FileNotFoundError, PermissionError) as e:
        logger_error(e, exc_info=True)
        await message.answer(f'<blockquote>{e}</blockquote>')
