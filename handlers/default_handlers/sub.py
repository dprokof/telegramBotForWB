import aiohttp
from aiogram import types, F
from aiogram.filters.callback_data import CallbackData
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config_data.config import API_KEY
from loader import dp, bot
from states.states_info import RegState


BASE_URL = 'https://supplies-api.wildberries.ru/api/v1/'
header = {
    'Authorization': API_KEY
}
supply_types = []


def get_id_by_name(data, name):
    for item in data:
        if item['name'] == name:
            return item['ID']


@dp.message(Command('sub'))
async def cmd_sub(message: types.Message, state: FSMContext):
    await message.answer('Назовите вашу подписку')
    await state.set_state(RegState.warehouse)


@dp.message(RegState.warehouse)
async def choose_warehouse(message: types.Message, state: FSMContext):
    await state.update_data(sub_name = message.text)
    global warehouses
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + 'warehouses', headers=header) as response:
            warehouses = await response.json()
    button_list = [warehouse['name'] for warehouse in warehouses]
    builder = ReplyKeyboardBuilder()
    for i in button_list:
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(3)
    await message.answer(
        'Выберите склад',
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(RegState.supply_type)


@dp.message(RegState.supply_type)
async def choose_supply_type(message: types.Message, state: FSMContext):
    warehouse_name = message.text
    print(warehouse_name)
    warehouse_id = get_id_by_name(warehouses, warehouse_name)
    print(warehouse_id)
    await state.update_data(warehouse_name=warehouse_name, warehouse_id=warehouse_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='Короба', callback_data='boxes'),
                types.InlineKeyboardButton(text='Монопаллеты', callback_data='monopallet'),
                types.InlineKeyboardButton(text='Суперсейф', callback_data='supersafe'),
                types.InlineKeyboardButton(text='QR - поставка с коробами', callback_data='QR'),
                types.InlineKeyboardButton(text='Готово', callback_data='ready'))
    builder.adjust(2)
    await message.answer(
        'Выберите тип(ы) поставки',
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == 'boxes')
async def button_boxes(callback):
    if 'Короба' not in supply_types:
        supply_types.append('Короба')
    else:
        supply_types.remove('Короба')
    await callback.answer()


@dp.callback_query(F.data == 'monopallet')
async def button_monopallet(callback):
    if 'Монопаллеты' not in supply_types:
        supply_types.append('Монопаллеты')
    else:
        supply_types.remove('Монопаллеты')
    await callback.answer()


@dp.callback_query(F.data == 'supersafe')
async def button_supersafe(callback):
    if 'Суперсейф' not in supply_types:
        supply_types.append('Суперсейф')
    else:
        supply_types.remove('Суперсейф')
    await callback.answer()


@dp.callback_query(F.data == 'QR')
async def button_QR(callback):
    if 'QR - поставка с коробами' not in supply_types:
        supply_types.append('QR - поставка с коробами')
    else:
        supply_types.remove('QR - поставка с коробами')
    await callback.answer()


@dp.callback_query(F.data == 'ready')
async def get_warehouse_name(message: types.Message, state: FSMContext):
    await state.update_data(supply_types=supply_types)
    builder = ReplyKeyboardBuilder()
    for i in range(21):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(5)
    await bot.send_message(
        text='Выберите минимальный коэффициент для данной подписки',
        reply_markup=builder.as_markup(resize_keyboard=True), chat_id=message.from_user.id
    )
    await state.set_state(RegState.min_coefficient)


@dp.message(RegState.min_coefficient)
async def choose_min_coefficient(message: types.Message, state: FSMContext):
    await state.update_data(min_coeff=message.text)
    builder = ReplyKeyboardBuilder()
    for i in range(21):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(5)
    await message.answer(
        text='Выберите максимальный коэффициент для данной подписки',
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(RegState.max_coefficient)


@dp.message(RegState.max_coefficient)
async def choose_max_coefficient(message: types.Message, state: FSMContext):
    await state.update_data(max_coeff=message.text)
    # data = await state.get_data()
    # header = {
    #     'Authorization': API_KEY
    # }
    # ID = data['warehouse_id']
    # url = f'https://supplies-api.wildberries.ru/api/v1/acceptance/coefficients?warehouseIDs={ID}'
    # print(url)
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url, headers=header, ) as response:
    #         info = await response.json()
    # print(info)
    data = await state.get_data()
    print(data)
    sub_name = data['sub_name']
    warehouse_name = data['warehouse_name']
    warehouse_id = data['warehouse_id']
    min_coeff = data['min_coeff']
    max_coeff = data['max_coeff']
    supply_types = data['supply_types']
    await message.answer("Подиска сохранена!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(
        f"Название подписки - {sub_name}\n"
        f"Название склада - {warehouse_name}\n"
        f"ID склада - {warehouse_id}\n"
        f"Тип(ы) упаковки - {supply_types}\n"
        f"Минимальный коэффициент - {min_coeff}\n"
        f"Максимальный коэффициент - {max_coeff}\n"
    )
    await state.clear()


