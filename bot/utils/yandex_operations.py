import yadisk
import aiofiles
import aiohttp
import hashlib
from config_reader import yandex_token, yandex_id, yandex_secret, YANDEX_FOLDER


async def upload_file_to_yandex_disk_and_get_link(local_file_path: str, timeout: int) -> str:
    """
    Загружает файл на Яндекс.Диск и возвращает сокращенную ссылку на него.

    :param local_file_path: Путь к загружаемому файлу.
    :param timeout: Время ожидания запроса.
    :return: Сокращенная ссылка на загруженный файл.
    """

    # Инициализация клиента Яндекс.Диска
    client = yadisk.AsyncClient(id=yandex_id,
                                secret=yandex_secret,
                                token=yandex_token)

    # Извлечение имени и расширения файла
    _, filename = local_file_path.rsplit('/', maxsplit=1)
    filename, extension = filename.rsplit('.', maxsplit=1)

    # Путь, куда будет загружен файл на Яндекс.Диск
    yandex_destination_path = f'/{YANDEX_FOLDER}/{filename}.some_other_extension'
    # Путь, по которому будет сгенерирована ссылка на скачивание
    yandex_file_path = f'/{YANDEX_FOLDER}/{filename}.{extension}'

    async with client:
        # Проверка существования папки на Яндекс.Диске и создание её, если она не существует
        if not await client.exists(YANDEX_FOLDER):
            await client.mkdir(YANDEX_FOLDER)

        try:
            yandex_file_hash = (await client.get_meta(yandex_file_path, fields=['md5']))['md5']
            local_file_hash = await get_file_hash(local_file_path)

            # Проверка изменений в файлах
            if yandex_file_hash != local_file_hash:
                # Загрузка файла на Яндекс.Диск
                async with aiofiles.open(local_file_path, "rb") as file_to_upload:
                    await client.upload(file_to_upload, yandex_destination_path, overwrite=True, timeout=timeout)

                # Удаление предыдущей версии файла
                await client.remove(yandex_file_path)
                # Переименование файла
                await client.rename(yandex_destination_path, f'{filename}.{extension}')

        except yadisk.exceptions.PathNotFoundError:
            # Загрузка файла на Яндекс.Диск
            async with aiofiles.open(local_file_path, "rb") as file_to_upload:
                await client.upload(file_to_upload, yandex_destination_path, timeout=timeout)

            # Переименование файла
            await client.rename(yandex_destination_path, f'{filename}.{extension}')

        # Получение прямой ссылки на загруженный файл
        yandex_download_link = await client.get_download_link(yandex_file_path)

    # Сокращение ссылки
    shortened_link = await shorten_url(yandex_download_link)

    return shortened_link


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


async def get_file_hash(path: str) -> str:  # Optional[str]:
    """
    Получает хеш файла.

    :param path: Путь к файлу.
    :return: Хеш файла #или None, если что-то пошло не так.
    """
    # try:
    async with aiofiles.open(path, 'rb') as file:
        data = await file.read()
        md5_hash = hashlib.md5(data).hexdigest()
        return md5_hash
    # except Exception as e:
    #     print(f"An error occurred while calculating the hash: {e}")
    #     return None
