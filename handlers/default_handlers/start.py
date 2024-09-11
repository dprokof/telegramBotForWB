import re
from aiogram import types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from loader import dp



@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f'Привет....\n')
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Отправить номер', request_contact=True))
    await message.answer(text='Пожалуйста, отправьте свой номер телефона для завершения регистрации',
                         reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.contact)
async def contact(message: types.Contact):
    await message.answer('Вы успешно прошли регистрацию!')
    await message.answer('Давайте создадим первую подписку для Вас\n'
                         'Для управления своими подписками используйте команду /sub')
