import aiohttp
import aiofiles
import yadisk
import asyncio
import time
import hashlib
from aiogram.types import Message

from keyboards.retrieve_file import get_progress_keyboard
from config_reader import yandex_token, yandex_id, yandex_secret, YANDEX_FOLDER
from main import logger, logger_error


class YandexUploader:
    CHUNK_SIZE = 4 * 2**20  # 4MB

    def __init__(self, path: str, filesize: int, message: Message, upload_speed: int = None):
        self.path = path
        self.filesize = filesize
        self.message = message
        self.upload_speed = upload_speed

        self.file_basename = path.rsplit('/', maxsplit=1)[1]
        self.filename, self.extension = self.file_basename.rsplit('.', maxsplit=1)

        self.yandex_dst_path = f'/{YANDEX_FOLDER}/{self.filename}.some_other_extension'
        self.yandex_src_path = f'/{YANDEX_FOLDER}/{self.filename}.{self.extension}'

        logger.info(f"YandexUploader initialized for {self.file_basename}, size: {self.filesize} bytes")

    @staticmethod
    def get_client() -> yadisk.AsyncClient:
        """Создает асинхронный клиент Yandex Disk"""
        return yadisk.AsyncClient(id=yandex_id, secret=yandex_secret, token=yandex_token)

    async def check_file_existence(self) -> bool:
        async with self.get_client() as client:
            if not await client.exists(YANDEX_FOLDER):
                logger.info(f"Folder {YANDEX_FOLDER} not found, creating...")
                await client.mkdir(YANDEX_FOLDER)

            try:
                yandex_file_hash = (await client.get_meta(self.yandex_src_path, fields=['md5']))['md5']
                logger.info(f"File {self.yandex_src_path} exists on Yandex Disk")
            except yadisk.exceptions.NotFoundError:
                logger.info(f"File {self.yandex_src_path} not found on Yandex Disk")
                return False

            local_file_hash = await get_file_hash(self.path)
            exists = local_file_hash == yandex_file_hash

            if exists:
                logger.info(f"File {self.file_basename} is identical to the one on Yandex Disk")
            else:
                logger.info(f"File {self.file_basename} differs from the one on Yandex Disk, will re-upload")

            return exists

    async def get_yandex_link(self) -> str:
        async with self.get_client() as client:
            yandex_download_link = await client.get_download_link(self.yandex_src_path)

        short_link = await shorten_url(yandex_download_link)
        logger.info(f"Generated short link for {self.file_basename}: {short_link}")
        return short_link

    async def _get_upload_url(self, client) -> str:
        """Получает URL для загрузки файла"""
        return await client.get_upload_link(self.yandex_dst_path, overwrite=True)

    async def upload_file_to_yandex_disk(self) -> None:
        """Загружает файл на Яндекс.Диск"""
        if await self.check_file_existence():
            logger.info(f"Skipping upload: {self.file_basename} is already up-to-date")
            return

        try:
            async with (self.get_client() as client,
                        aiohttp.ClientSession() as session,
                        aiofiles.open(self.path, "rb") as file):
                upload_url = await self._get_upload_url(client)
                headers = {"Content-Length": str(self.filesize)}

                logger.info(f"Uploading {self.file_basename} to {self.yandex_dst_path}...")
                await session.put(upload_url, data=self.stream_reader(file), headers=headers)

                await client.rename(self.yandex_dst_path, self.file_basename)
                logger.info(f"Upload complete: {self.file_basename} -> {self.yandex_src_path}")

        except Exception as e:
            logger_error(f"Error uploading {self.file_basename}", exc_info=True)

    async def stream_reader(self, file):
        """Асинхронный итератор для чтения чанков с контролем скорости"""
        uploaded = 0
        last_update_time = time.time()
        update_interval = 2
        sleep_time = self.CHUNK_SIZE / self.upload_speed if self.upload_speed else 0

        try:
            while chunk := await file.read(self.CHUNK_SIZE):
                uploaded += len(chunk)

                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)

                    if time.time() - last_update_time >= update_interval:
                        progress = f"{uploaded / self.filesize * 100:.2f}%"
                        await self.message.edit_text(text=self.message.html_text,
                                                     reply_markup=get_progress_keyboard(f"{progress}..."))
                        last_update_time = time.time()

                yield chunk

        except OSError as e:
            logger_error(f"Error reading file {self.file_basename}: {e}")
        except Exception as e:
            logger_error(f"Unexpected error while streaming {self.file_basename}: {e}")
        finally:
            await file.close()
            logger.info(f"Finished reading {self.file_basename}")


async def shorten_url(long_url: str) -> str:
    """
    Сокращает указанную ссылку с использованием сервиса 'https://clck.ru' и возвращает сокращенную ссылку.

    :param long_url: Ссылка, которую нужно сократить.
    :return: Сокращенная ссылка.
    """

    endpoint = 'https://clck.ru/--'
    params = {'url': long_url + '?utm_source=sender'}

    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint, params=params) as response:
            shortened_url = await response.text()

            return shortened_url


async def get_file_hash(path: str) -> str:
    """
    Получает хеш файла.

    :param path: Путь к файлу.
    :return: Хеш файла #или None, если что-то пошло не так.
    """

    async with aiofiles.open(path, 'rb') as file:
        data = await file.read()
        md5_hash = hashlib.md5(data).hexdigest()

        return md5_hash
