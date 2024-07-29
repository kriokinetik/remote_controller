import os
import shutil


def is_hidden_file(file_path: str) -> bool:
    """
    Проверяет, является ли файл скрытым.

    :param file_path: Путь к файлу.
    :return: True, если файл скрыт, иначе False.
    """

    try:
        # Получаем атрибуты файла
        attributes = os.stat(file_path).st_file_attributes
        # Проверяем, является ли файл скрытым
        return attributes & 2 == 2
    except OSError as e:
        print(f'Error: {e}')
        return False


def is_ignored_folders(folder_name: str) -> bool:
    """Проверяет, находится ли папка в игнор-листе."""

    ignored_folders = ['Documents and Settings', 'ESD', 'Intel', 'MC12demo', 'PerfLogs']
    ignored_prefixes = ('.', '$', 'Windows')  # Список игнорируемых папок
    return folder_name.startswith(ignored_prefixes) or folder_name in ignored_folders


def is_ignored_document(document_name: str) -> bool:
    """Проверяет, находится ли файл в игнор-листе."""

    # Список игнорируемых расширений файлов
    ignored_extensions = ('.tmp', '.bak', '.old', '.ini', '.lnk', '.pri', '.lst', '.SFX', '.dat')
    ignored_prefixes = ('~', '.')  # Префиксы, которые должны игнорироваться
    return document_name.endswith(ignored_extensions) or document_name.startswith(ignored_prefixes)


def sort_documents_in_directory(directory_path: str) -> (list, list):
    """
    Сортирует документы и папки в указанной директории.

    :param directory_path: Путь к директории.
    :return: Кортеж, содержащий отсортированные списки папок и документов.
    """

    folders, documents = [], []
    # Проходим по всем элементам в директории
    for item in os.scandir(directory_path):
        # Проверяем, не скрыт ли файл
        if not is_hidden_file(os.path.join(directory_path, item.name)):
            # Если это папка и не находится в игнор-листе
            if item.is_dir() and not is_ignored_folders(item.name):
                folders.append(f'{item.name}\\')
            # Если это файл и не находится в игнор-листе, добавляем его в список документов
            elif item.is_file() and not is_ignored_document(item.name):
                documents.append(f'• <code>{item.name}</code>')
    return sorted(folders), sorted(documents)


def generate_directory_info(current_directory: str) -> (str, list[str]):
    """
    Возвращает список документов и папок в текущей директории.

    :param current_directory: Текущий путь.
    :return: Кортеж, содержащий строку с информацией о текущем пути и список папок.
    """

    # Сортируем документы и папки в текущей директории
    folders, documents = sort_documents_in_directory(current_directory)
    # Возвращаем строку с информацией о текущем пути и список папок
    return ((f'<code>{current_directory}</code>\n'
            f'────────────────────────\n') + '\n'.join(documents),
            folders)


def get_desktop_path() -> str:
    """
    Получает путь к рабочему столу пользователя.

    :return: Путь к рабочему столу пользователя.
    """

    return os.path.join(os.path.expanduser("~"), "Desktop") + '\\'


def get_file_or_directory_size(path: str) -> int:
    """
    Получает размер файла или директории.

    :param path: Путь к файлу или директории.
    :return: Размер файла или директории в байтах.
    """

    if os.path.isfile(path):
        # Если путь указывает на файл, возвращаем его размер
        return os.path.getsize(path)
    else:
        size = 0
        # Если путь указывает на директорию, рекурсивно считаем размер всех файлов в ней
        for folder_path, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(folder_path, file)
                size += os.stat(file_path).st_size
        return size


def compress_folder_to_zip(folder_path: str) -> str:
    """
    Архивирует содержимое папки в формате .zip.

    :param folder_path: Путь к папке, которую нужно архивировать.
    :return: Путь к созданному архиву .zip.
    """

    _, folder_name = folder_path[:-1].rsplit('/', maxsplit=1)
    archive_folder_path = f'../misc/{folder_name}'

    if not os.path.exists(f'{archive_folder_path}.zip'):
        shutil.make_archive(archive_folder_path, 'zip', folder_path)

    return f'{archive_folder_path}.zip'


def get_archive_folder_path(folder_name):
    return f'../misc/{folder_name}.zip'
