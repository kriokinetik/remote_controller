import ctypes
import io
import win32gui
import win32ui
from PIL import Image, ImageGrab


def get_cursor_image():
    """
    Получает изображение текущего курсора и его позицию hotspot.

    :return: Кортеж, содержащий изображение курсора и его позицию hotspot.
    """

    cursor_info = win32gui.GetCursorInfo()
    hcursor = cursor_info[1]
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 36, 36)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), hcursor)

    bmp_info = hbmp.GetInfo()
    bmp_str = hbmp.GetBitmapBits(True)
    cursor_image = Image.frombuffer("RGB", (bmp_info["bmWidth"], bmp_info["bmHeight"]),
                                    bmp_str, "raw", "BGRX", 0, 1).convert("RGBA")

    win32gui.DestroyIcon(hcursor)
    win32gui.DeleteObject(hbmp.GetHandle())
    hdc.DeleteDC()

    # Прозрачность для курсора
    pixdata = cursor_image.load()
    width, height = cursor_image.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (0, 0, 0, 255):
                pixdata[x, y] = (0, 0, 0, 0)

    # Получаем позицию hotspot
    hotspot = win32gui.GetIconInfo(hcursor)[1:3]

    return cursor_image, hotspot


def overlay_cursor_on_screenshot(parameter: bool) -> io.BytesIO:
    """
    Налагает изображение курсора на скриншот.

    :param parameter: Флаг, указывающий, следует ли включать курсор на скриншот.
    :return: Скриншот с наложенным курсором в формате BytesIO.
    """

    # Получаем скриншот экрана
    screenshot = ImageGrab.grab(bbox=None, include_layered_windows=True)

    if parameter:
        # Получаем изображение курсора и его позицию
        cursor_image, (hotspot_x, hotspot_y) = get_cursor_image()
        # Получаем масштабированные координаты курсора
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        cursor_position_win = win32gui.GetCursorPos()
        cursor_position = (round(cursor_position_win[0] * scale_factor - hotspot_x),
                           round(cursor_position_win[1] * scale_factor - hotspot_y))
        # Накладываем изображение курсора на скриншот
        screenshot.paste(cursor_image, cursor_position, cursor_image)

    # Создаем поток BytesIO для сохранения скриншота
    output = io.BytesIO()
    screenshot.save(output, "png")

    return output
