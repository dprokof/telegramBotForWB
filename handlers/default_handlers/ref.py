from aiogram import types, F
from aiogram.filters.command import Command
from loader import dp, bot
from aiogram.utils.deep_linking import create_start_link


@dp.message(Command('ref'))
async def cmd_ref(message: types.Message):
    await message.answer('Поздравляем, Вы получили реферальную ссылку.\n'
                         'По данной ссылке ваши знакомые смогут использовать бота 14 дней, вместо 3')
    link = await create_start_link(bot, str(message.from_user.id), encode=True)
    await message.answer(link)