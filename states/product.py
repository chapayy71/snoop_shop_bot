from aiogram.fsm.state import State, StatesGroup


class ProductAdd(StatesGroup):
    category = State()
    name = State()
    description = State()
    price = State()
    stock = State()

class ProductDelete(StatesGroup):
    id = State()

class ProductEdit(StatesGroup):
    price = State()
    stock = State()