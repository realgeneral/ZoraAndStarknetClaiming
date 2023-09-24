from aiogram.dispatcher.filters.state import State, StatesGroup


class ToEarn(StatesGroup):
    admin_menu = State()
    add_user = State()

