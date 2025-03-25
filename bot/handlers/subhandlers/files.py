import asyncio
import os
import time
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest

from tools import YandexUploader, file_ops, logger, speedtest
from bot.states import DataStates
from bot import keyboards
from config import MAX_SIZE, PAGE_SIZE

router = Router()


def get_navigation_text(path: str, files: list, page_id: int) -> str:
    space_line = "\u2500" * 24
    header_text = f"<code>{path}</code>\n{space_line}"

    if not files:
        return f"{header_text}\n{space_line}\nНет файлов в директории\n"

    file_pages = file_ops.chunk_list(files, PAGE_SIZE)
    files_text_list = "\n".join(file_pages[page_id]) if file_pages else ""
    start_index = page_id * PAGE_SIZE + 1
    end_index = min((page_id + 1) * PAGE_SIZE, len(files))
    page_indicator = f"Показаны файлы {start_index}-{end_index} из {len(files)}"
    return f"{header_text}\n{files_text_list}\n{space_line}\n{page_indicator}"


async def navigate_to_path(callback: CallbackQuery, state: FSMContext, path: str):
    try:
        await state.update_data(path=path)
        folders, files = file_ops.get_directory_info(path)
        file_pages = file_ops.chunk_list(files, PAGE_SIZE)
        pages_count = len(file_pages)
        await state.update_data(pages_count=pages_count, page_id=0)
        text = get_navigation_text(path, files, 0)
        await callback.message.edit_text(text=text, reply_markup=keyboards.files.next_directory(folders, pages_count > 1))
        await callback.answer()
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback.answer(f"Message is not modified")
            return
        logger.logger_error(e, exc_info=True)
        await callback.message.answer(f"<blockquote>{e}</blockquote>")
    except (PermissionError, FileNotFoundError) as e:
        logger.logger_error(e, exc_info=True)
        await callback.message.answer(f"<blockquote>{e}</blockquote>")


@router.callback_query(F.data == "traverse_up_directory")
async def handle_traverse_up_directory(callback: CallbackQuery, state: FSMContext):
    current_path = (await state.get_data()).get("path", "")
    if current_path in ["D:\\", "C:\\"]:
        await callback.answer()
        return
    next_path = os.path.abspath(os.path.join(current_path, "..")) + os.sep
    await navigate_to_path(callback, state, next_path)


@router.callback_query(F.data.in_({"D:\\", "C:\\"}))
async def handle_traverse_up_to_disk(callback: CallbackQuery, state: FSMContext):
    await navigate_to_path(callback, state, callback.data)


@router.callback_query(F.data.endswith(os.sep))
async def handle_traverse_directory(callback: CallbackQuery, state: FSMContext):
    current_path = (await state.get_data()).get("path", "")
    next_path = os.path.join(current_path, callback.data)
    await navigate_to_path(callback, state, next_path)


@router.callback_query(F.data.in_({"next_page", "prev_page"}))
async def navigate_pages_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_path, page_id, pages_count = data.get("path", ""), data.get("page_id", 0), data.get("pages_count", 1)
    folders, files = file_ops.get_directory_info(current_path)
    file_pages = file_ops.chunk_list(files, PAGE_SIZE)
    page_id = (page_id + 1) % pages_count if callback.data == "next_page" else (page_id - 1) % pages_count
    await state.update_data(page_id=page_id)
    text = get_navigation_text(current_path, files, page_id)
    await callback.message.edit_text(text=text, reply_markup=keyboards.files.next_directory(folders, True))


@router.message(DataStates.path)
async def handle_send_document(message: Message):
    logger.logger_event_info(message)

    try:
        path = message.text.replace("\\", "/")
        filesize = file_ops.get_file_or_directory_size(path)

        if os.path.isfile(path):
            _, filename = path.rsplit("/", maxsplit=1)
            is_file = True
        elif os.path.isdir(path):
            await message.reply(f"Архивируется...")
            path = file_ops.compress_folder_to_zip(path)
            _, filename = path.rsplit("/", maxsplit=1)
            filesize = os.path.getsize(path)
            is_file = False
        else:
            await message.reply("Указанный путь не существует или не является доступным файлом/папкой")
            return

        if filesize < MAX_SIZE:
            await message.reply(f"Файл <code>{filename}</code> загружается...\n")
            await message.reply_document(document=FSInputFile(path=path))
        else:
            internet_speed_task = asyncio.create_task(speedtest.measure_speed("upload", False))

            rounded_filesize = speedtest.humansize(filesize)

            download_message = await message.reply(f"Файл <code>{filename}</code> загружается на Яндекс.Диск...\n"
                                                   f"Размер файла: <code>{rounded_filesize}</code>\n"
                                                   f"Время ожидания: —",
                                                   reply_markup=keyboards.files.get_progress_keyboard("..."))

            yandex_uploader = YandexUploader(path, filesize, download_message)

            if not await yandex_uploader.check_file_existence():
                try:
                    internet_speed = await internet_speed_task
                    logger.logger_info(f"Upload speed: {internet_speed}")

                    upload_time = filesize / internet_speed
                    estimated_time = time.strftime("%H:%M:%S", time.gmtime(upload_time))

                    yandex_uploader.upload_speed = internet_speed

                except ValueError as e:
                    estimated_time = "N/A"
                    logger.logger_error(e)

                download_message = await download_message.edit_text(f"Файл: <code>{filename}</code>\n"
                                                                    f"Размер файла: <code>{rounded_filesize}</code>\n"
                                                                    f"Время ожидания: {estimated_time}",
                                                                    reply_markup=download_message.reply_markup
                                                                    )

                yandex_uploader.message = download_message

                await yandex_uploader.upload_file_to_yandex_disk()
                logger.logger_info(f"Start uploading file '{path}' (size: {filesize} bytes) to Yandex Disk")  # logging

            download_link = await yandex_uploader.get_yandex_link()
            logger.logger_info(f"File '{path}' (size: {filesize} bytes) has been successfully uploaded to Yandex Disk")
            await download_message.edit_text(f"Файл: <code>{filename}</code>\n"
                                             f"Размер файла: <code>{rounded_filesize}</code>",
                                             reply_markup=keyboards.files.get_progress_keyboard(
                                                 "Скачать файл...", download_link)
                                             )
        if not is_file:
            os.remove(path)

    except (FileNotFoundError, PermissionError) as e:
        logger.logger_error(e, exc_info=True)
        await message.answer(f"<blockquote>{e}</blockquote>")
