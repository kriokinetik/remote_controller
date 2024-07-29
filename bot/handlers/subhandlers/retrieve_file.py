from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest
import os

from main import logger_info, logger_error, logger
from states import DataStates
from utils import file_operations, yandex_operations
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
        # Получаем путь к файлу или папке из сообщения
        path = message.text.replace('\\', '/')
        # Получаем размер файла или папки
        filesize = file_operations.get_file_or_directory_size(path)
        # Округленный размер файла в мегабайтах
        rounded_filesize = round(filesize / 2 ** 20, 1)
        # Примерное время ожидания загрузки документа
        estimated_time = round(rounded_filesize / 5)

        if os.path.isfile(path):
            # Название документа
            _, filename = path.rsplit('/', maxsplit=1)
            # Если это файл и его размер меньше максимального
            if filesize < MAX_SIZE:
                await message.reply(f'Файл <code>{filename}</code> загружается...\n')
                await message.reply_document(document=FSInputFile(path=path))

            # Если файл слишком большой, загружаем его на Яндекс.Диск
            else:
                download_message = await message.reply(f'Файл <code>{filename}</code> загружается на Яндекс.Диск...\n'
                                                       f'Размер файла: <code>{rounded_filesize} MB</code>\n'
                                                       f'Примерное время ожидания: {estimated_time} сек'
                                                       )
                logger.info(f'Start uploading file "{path}" (size: {filesize} bytes) to Yandex Disk')  # logging
                download_link = await yandex_operations.upload_file_to_yandex_disk_and_get_link(path, estimated_time)
                logger.info(f'File "{path}" (size: {filesize} bytes) has been successfully uploaded to Yandex Disk')
                await download_message.edit_text(f'Файл: <code>{filename}</code>\n'
                                                 f'Размер файла: <code>{rounded_filesize} MB</code>\n\n'
                                                 f'<a href="{download_link}">Скачать файл...</a>'
                                                 )

        elif os.path.isdir(path):
            # Название папки
            _, foldername = path[:-1].rsplit('/', maxsplit=1)
            # Если это папка, сжимаем её в ZIP
            logger.info(f'Folder "{path}" is being compressed')  # logging
            await message.reply(f'Папка <code>{foldername}</code> архивируется...\n'
                                f'Размер папки: <code>{rounded_filesize} MB</code>'
                                )
            archive_path = file_operations.compress_folder_to_zip(path)
            logger.info(f'Folder "{path}" has been archived successfully')  # logging
            # Если размер архива меньше максимального, отправляем как документ
            if os.path.getsize(archive_path) < MAX_SIZE:
                await message.reply_document(document=FSInputFile(path=archive_path))

            # Иначе загружаем архив на Яндекс.Диск
            else:
                download_message = await message.reply(
                    f'Архив <code>{foldername}</code> загружается на Яндекс.Диск...\n'
                    f'Размер архива: <code>{rounded_filesize} MB</code>\n'
                    f'Примерное время ожидания: {estimated_time} сек'
                )
                logger.info(f'Start uploading archive "{foldername}" (size: {filesize} bytes) to Yandex '
                            f'Disk')  # logging
                download_link = await yandex_operations.upload_file_to_yandex_disk_and_get_link(archive_path,
                                                                                                estimated_time)
                logger.info(f'Archive "{foldername}" (size: {filesize} bytes) has been successfully uploaded to Yandex '
                            f'Disk')  # logging
                await download_message.edit_text(f'Архив: <code>{foldername}</code>\n'
                                                 f'Размер архива: <code>{rounded_filesize} MB</code>\n\n'
                                                 f'<a href="{download_link}">Скачать архив...</a>'
                                                 )

            # Удаляем временный архив
            os.remove(archive_path)

    except (FileNotFoundError, PermissionError) as e:
        logger_error(e, exc_info=True)
        await message.answer(f'<blockquote>{e}</blockquote>')
