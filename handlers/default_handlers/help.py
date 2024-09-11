from aiogram import types, F
from aiogram.filters.command import Command
from config_data.config import DEFAULT_COMMANDS
from loader import dp

@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    await message.reply("\n".join(text))
