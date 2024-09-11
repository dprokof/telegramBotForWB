from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State


class RegState(StatesGroup):
    phone = State()
    warehouse = State()
    supply_type = State()
    get_warehouse_id = State()
    supply_coefficient = State()
    min_coefficient = State()
    max_coefficient = State()
    preview = State()

class MyCallBack(CallbackData, prefix='my'):
    foo: str

