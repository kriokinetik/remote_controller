from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import pyautogui

from tools.logger import logger_event_info
from bot.filters import BotAccessFilter

router = Router()


@router.message(Command("help"), BotAccessFilter())
async def help_hanlder(message: Message):
    logger_event_info(message)

    await message.answer(
        "I can assist you with managing your computer remotely. Use these commands to control the device:\n\n"
        "<b>📁 File & Directory</b>\n"
        "/cd - navigate to a directory\n"
        "/sendfile - send a file\n\n"
        "<b>🖱️ Remote Control</b>\n"
        "/remote - send the control panel\n"
        "/minimize - minimize or restore all windows\n\n"
        "<b>🖼️ Screen & Network</b>\n"
        "/screenshot - take a screenshot\n"
        "/speedtest - test internet speed\n\n"
        "<b>🔐 System</b>\n"
        "/lock - lock the computer\n"
        "/restart - restart the computer\n"
        "/shutdown - shutdown the computer\n\n"
        "<b>❓ Help</b>\n"
        "/help_cd - instructions for /cd command\n"
        "/help_cursor - instructions for cursor control\n\n"
        "💡 You can also move the cursor by simply sending two numbers like <code>400 300</code>"
    )


@router.message(Command("help_cursor"), BotAccessFilter())
async def help_cursor_handler(message: Message):
    logger_event_info(message)

    bound_x, bound_y = pyautogui.size()

    await message.answer(
        f"📍 To move the cursor, just send a message with coordinates, "
        f"following the format and limits below:\n\n"
        f"↔️ x: <code>1 — {bound_x - 1}</code>\n"
        f"↕️ y: <code>1 — {bound_y - 1}</code>\n\n"
        f"Format: <code>x y</code>\n"
    )


@router.message(Command("help_cd"), BotAccessFilter())
async def help_cd_handler(message: Message):
    logger_event_info(message)

    await message.answer(
        "<b>cd</b>\n"
        "Displays the name of the current directory or changes the current directory. "
        "If used with only a drive letter (for example, <code>/cd C:</code>), "
        "cd displays the names of the current directory in the specified drive.\n\n"
        
        "<b>Syntax</b>\n"
        "<pre>/cd &lt;directory path&gt;</pre>\n\n"
        
        "<b>Examples</b>\n"
        "1. To navigate to the directory <code>C:\\Program Files</code>:\n"
        "<pre>/cd C:\\Program Files</pre>"
        "2. To move one level up:\n"
        "<pre>/cd ..</pre>"
        "3. To return to the root directory, the top of the directory hierarchy for a drive:\n"
        "<pre>/cd \\</pre>\n\n"
        
        "<b>Using relative paths</b>\n"
        "You can use relative paths to navigate within directories relative to your current location.\n"
        "1. To move into a <code>subdirectory</code>:\n"
        "<pre>/cd subdirectory</pre>"
        "2. To move up one level and then into another subdirectory:\n"
        "<pre>/cd ..\\other_directory</pre>\n\n"
        
        "<b>Remarks</b>\n"
        "- The command works only with directories that are accessible on the device.\n"
        "- To change the drive, specify the drive letter followed by a colon and backslash (e.g., <code>/cd C:\\</code> or <code>/cd D:\\</code>)."
    )
