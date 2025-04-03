import asyncio
import os
import time
from aiogram import Router, F
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest

import tools.file_ops
from tools import YandexUploader, file_ops, logger, speedtest
from bot.filters import BotAccessFilter
from bot import keyboards
from config import MAX_SIZE, PAGE_SIZE

router = Router()


def get_navigation_text(path: str, items: list, page_id: int, mode: str) -> str:
    emoji = "📁" if mode == "folder" else "🔖"
    header_text = f"{emoji} <code>{path}</code>"

    if not items:
        return f"{header_text}\n\n<i>📎 No {mode}s in the directory</i>\n"

    item_pages = file_ops.chunk_list(items, PAGE_SIZE)
    items_text_list = "\n".join(item_pages[page_id]) if item_pages else ""

    start_index = page_id * PAGE_SIZE + 1
    end_index = min((page_id + 1) * PAGE_SIZE, len(items))

    page_indicator = f"📎 <i>Showing {mode}s {start_index}-{end_index} of {len(items)}</i>"

    return f"{header_text}\n\n{items_text_list}\n\n{page_indicator}"


async def navigate_to_path(message, state: FSMContext, edit: bool = False):
    try:
        mode = (await state.get_data()).get("mode", "folder")
        path = (await state.get_data()).get("path")

        folders, files = file_ops.get_directory_info(path)
        items = folders if mode == "folder" else files
        item_pages = file_ops.chunk_list(items, PAGE_SIZE)
        pages_count = len(item_pages)

        await state.update_data(pages_count=pages_count, page_id=0)
        text = get_navigation_text(path, items, page_id=0, mode=mode)

        if edit:
            await message.edit_text(text=text,
                                 reply_markup=keyboards.files.get_files_manager_keyboard(mode, pages=pages_count > 1))
        else:
            await message.answer(text=text,
                                    reply_markup=keyboards.files.get_files_manager_keyboard(mode, pages=pages_count > 1))

    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await message.answer(f"Message is not modified")
            return

        logger.logger_error(e, exc_info=True)
        await message.answer(f"<blockquote>{e}</blockquote>")

    except (PermissionError, FileNotFoundError) as e:
        logger.logger_error(e, exc_info=True)
        await message.answer(f"<blockquote>{e}</blockquote>")


@router.message(Command("cd"), BotAccessFilter())
async def cd_handler(message: Message, command: CommandObject, state: FSMContext):
    current_path = (await state.get_data()).get("path", "")
    relative_path = command.args if command.args is not None else tools.file_ops.get_desktop_path()

    if relative_path[1] == ":" and len(relative_path) <= 3:
        if len(relative_path) == 2:
            relative_path += os.sep

        if relative_path not in file_ops.get_drives():
            await message.reply("❌ Cannot find the drive specified")
            return

    next_path = os.path.abspath(os.path.join(current_path, relative_path))

    if not os.path.exists(next_path):
        await message.reply("❌ Cannot find the path specified.")
        return

    await state.update_data(path=next_path, mode="folder")
    await navigate_to_path(message, state)


@router.callback_query(F.data.in_({"show_folder", "show_file"}))
async def switch_files_folders_handler(callback: CallbackQuery, state: FSMContext):
    mode = callback.data.split("_")[1]
    await state.update_data(mode=mode)
    await navigate_to_path(callback.message, state, edit=True)


@router.callback_query(F.data.in_({"next_page", "prev_page"}))
async def navigate_pages_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    current_path = data.get("path", "")
    page_id = data.get("page_id", 0)
    pages_count = data.get("pages_count", 1)
    mode = data.get("mode", "folder")
    folders, files = file_ops.get_directory_info(current_path)
    items = folders if mode == "folder" else files
    page_id = (page_id + 1) % pages_count if callback.data == "next_page" else (page_id - 1) % pages_count

    await state.update_data(page_id=page_id)
    text = get_navigation_text(current_path, items, page_id, mode)

    await callback.message.edit_text(text=text, reply_markup=keyboards.files.get_files_manager_keyboard(mode, pages=True))


@router.message(Command("sendfile"), BotAccessFilter())
async def handle_send_document(message: Message, command: CommandObject, state: FSMContext):
    logger.logger_event_info(message)

    if command.args is None:
        await message.reply("💡 Usage example:\n<pre>/sendfile &lt;path&gt;</pre>")
        return

    current_path = (await state.get_data()).get("path", "")
    relative_path = command.args
    path = os.path.abspath(os.path.join(current_path, relative_path))

    try:
        filesize = file_ops.get_file_or_directory_size(path)

        if os.path.isfile(path):
            _, filename = path.rsplit(os.sep, maxsplit=1)
            is_file = True
        elif os.path.isdir(path):
            archiving_message = await message.reply("🔄 Archiving...")
            path = file_ops.compress_folder_to_zip(path)
            _, filename = path.rsplit(os.sep, maxsplit=1)
            filesize = os.path.getsize(path)
            is_file = False
            await archiving_message.delete()
        else:
            await message.reply("❌ The specified path does not exist or is not an accessible file/folder")
            return

        if filesize < MAX_SIZE:
            download_message = await message.reply(f"🔄 File <code>{filename}</code> is uploading...\n")
            await message.reply_document(document=FSInputFile(path=path))
            await download_message.delete()
        else:
            internet_speed_task = asyncio.create_task(speedtest.measure_speed("upload", False))

            rounded_filesize = speedtest.humansize(filesize)

            download_message = await message.reply(
                f"🔄 File <code>{filename}</code> is uploading to Yandex.Disk...\n"
                f"📏 Size: <code>{rounded_filesize}</code>\n"
                f"⏳ Estimated time: —",
                reply_markup=keyboards.files.get_progress_keyboard("...")
            )

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

                download_message = await download_message.edit_text(
                    f"📂 File: <code>{filename}</code> is uploading to Yandex.Disk...\n"
                    f"📏 Size: <code>{rounded_filesize}</code>\n"
                    f"⏳ Estimated time: {estimated_time}",
                    reply_markup=download_message.reply_markup)

                yandex_uploader.message = download_message

                await yandex_uploader.upload_file_to_yandex_disk()
                logger.logger_info(f"Start uploading file '{path}' (size: {filesize} bytes) to Yandex Disk")  # logging

            download_link = await yandex_uploader.get_yandex_link()
            logger.logger_info(f"File '{path}' (size: {filesize} bytes) has been successfully uploaded to Yandex Disk")
            await download_message.edit_text(f"📂 File: <code>{filename}</code>\n"
                                             f"📏 Size: <code>{rounded_filesize}</code>",
                                             reply_markup=keyboards.files.get_progress_keyboard(
                                                 "⬇️ Download file...", download_link)
                                             )
        if not is_file:
            os.remove(path)

    except (FileNotFoundError, PermissionError) as e:
        logger.logger_error(e, exc_info=True)
        await message.answer(f"<blockquote>{e}</blockquote>")
