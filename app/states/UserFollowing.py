from aiogram.dispatcher.filters.state import State, StatesGroup


class UserFollowing(StatesGroup):
    start_navigation = State()
    check_claim_net = State()
    check_subscribe = State()
    get_private_keys = State()
    choose_point = State()
    wallet_menu = State()
    new_private = State()
    tap_to_earn = State()
    create_session = State()
    choose_bridge = State()
    tap_to_earn_stark = State()
    check_ready = State()

