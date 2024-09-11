from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from config_data import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())