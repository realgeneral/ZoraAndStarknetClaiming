from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminMode(StatesGroup):
    admin_menu = State()
    add_user = State()
    add_money = State()
    set_new_price = State()
    send_alert = State()
