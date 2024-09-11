from aiogram.types import BotCommand
from config_data.config import DEFAULT_COMMANDS
from loader import bot


async def set_default_commands():
    bot_commands = [BotCommand(command=f'{cmd}', description=f'{des}') for cmd, des in DEFAULT_COMMANDS]
    await bot.set_my_commands(bot_commands)