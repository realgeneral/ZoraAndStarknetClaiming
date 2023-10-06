import datetime

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

from app.create_bot import dp
from app.states import AdminMode
from app.handlers.start_cmd import user_db

_one_wallet_run_price = 5


def get_one_wallet_run_price():
    return int(_one_wallet_run_price)


def set_one_wallet_run_price(value):
    global _one_wallet_run_price
    _one_wallet_run_price = value


@dp.message_handler(Text(equals=["⬅ Go to admin menu"]), state=AdminMode.admin_menu)
async def go_admin_menu(message: types.Message):
    await send_admin_menu(message)


@dp.message_handler(commands=['admin'], state='*')
async def send_admin_menu(message: types.Message):
    if int(message.from_user.id) == 420881832 or int(message.from_user.id) == 740574479 or int(
            message.from_user.id) == 812233995:
        message_response = "# *ADMIN MODE* \n"

        b1 = KeyboardButton("Increase max. wallets count")
        b2 = KeyboardButton("User list")
        b3 = KeyboardButton("Today logs")
        b4 = KeyboardButton("Users statistic")
        b7 = KeyboardButton("Сonfig settings")
        b8 = KeyboardButton("🔐 DATA DUMP")
        b6 = KeyboardButton("Give money")
        b5 = KeyboardButton("⬅ Go to menu")

        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.row(b1).row(b2, b4).row(b6, b3).row(b7, b8).row(b5)

        await AdminMode.admin_menu.set()
        await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN, reply_markup=buttons)


# ================================================= Сonfig settings ================================================


@dp.message_handler(Text(equals="Сonfig settings"), state=AdminMode.admin_menu)
async def send_new_price(message: types.Message):
    message_response = "Submit a new price for one wallet run"

    await AdminMode.set_new_price.set()
    await message.answer(message_response, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=AdminMode.set_new_price)
async def save_new_price(message: types.Message):

    global one_wallet_run_price
    try:
        one_wallet_run_price = int(message.text)
        message_response = f"*[SUCCESS]:* New one wallet price: _{one_wallet_run_price}_"
    except Exception as err_:
        message_response = f"*[ERROR]:* {err_}"

    buttons = [
        KeyboardButton(text="⬅ Go to admin menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    print(f"one_wallet_run_price admin - {one_wallet_run_price}")
    await AdminMode.admin_menu.set()
    await message.answer(message_response, reply_markup=reply_markup, parse_mode=types.ParseMode.MARKDOWN)


# ===============================================================================================================

# =================================================GIVE MONEY================================================

@dp.message_handler(Text(equals="Give money"), state=AdminMode.admin_menu)
async def send_money_to_user(message: types.Message):
    print(f"one_wallet_run_price admin - {one_wallet_run_price}")
    message_response = "Send user telegram_id:adding_usd"

    await AdminMode.add_money.set()
    await message.answer(message_response, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=AdminMode.add_money)
async def save_user_money(message: types.Message):
    try:
        telegram_id, money_usdt = message.text.split(':')
        user_db.update_balance(telegram_id, float(money_usdt))
        message_response = f"*[SUCCESS]:* To `{telegram_id}` added _{money_usdt}$_"
    except Exception as err_:
        message_response = f"*[ERROR]:* {err_}"

    buttons = [
        KeyboardButton(text="⬅ Go to admin menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    await AdminMode.admin_menu.set()
    await message.answer(message_response, reply_markup=reply_markup, parse_mode=types.ParseMode.MARKDOWN)


# ===============================================================================================================


# =========================================Increase max. wallets count ================================================

@dp.message_handler(Text(equals="Increase max. wallets count"), state=AdminMode.admin_menu)
async def add_prem_user(message: types.Message):
    message_response = "Send user telegream_id:wallets_count"

    await AdminMode.add_user.set()
    await message.answer(message_response, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=AdminMode.add_user)
async def save_prem_user(message: types.Message):
    try:
        telegram_id, wallets_count = message.text.split(':')
        user_db.set_max_wallets_count(telegram_id, int(wallets_count))

        message_response = f"*[SUCCESS]:* To `{telegram_id}` set wallets count: _{wallets_count}$_"
    except Exception as err_:
        message_response = f"*[ERROR]:* {err_}"
    buttons = [
        KeyboardButton(text="⬅ Go to admin menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    await AdminMode.admin_menu.set()
    await message.answer(message_response, reply_markup=reply_markup, parse_mode=types.ParseMode.MARKDOWN)


# ===============================================================================================================

@dp.message_handler(Text(equals="Today logs"), state=AdminMode.admin_menu)
async def get_today_logs(message: types.Message):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    today_logs = []

    with open("logs/logs.log", 'r') as f:
        for line in f:
            if today in line:
                today_logs.append(line.strip())

    reply_message = "\n".join(today_logs)

    if reply_message == "":
        reply_message = f"*[INFO]:* _Today no new logs..._"

    await message.answer(reply_message[-4000:], parse_mode=types.ParseMode.MARKDOWN)


# ===============================================================================================================


@dp.message_handler(Text(equals="Users statistic"), state=AdminMode.admin_menu)
async def get_user_statistic(message: types.Message):
    # Получить общее количество пользователей
    total_users = len(user_db.get_all_users())

    # Получить количество активных пользователей за разные интервалы времени
    active_users_1_day = user_db.get_active_users_count(1)
    active_users_3_days = user_db.get_active_users_count(3)
    active_users_7_days = user_db.get_active_users_count(7)

    # Формирование текста статистики
    stats_text = f"""
        📊 User Statistics 📊

    🔹 Total number of users: {total_users}
    🔹 Active users in the last day: {active_users_1_day}
    🔹 Active users in the last 3 days: {active_users_3_days}
    🔹 Active users in the last week: {active_users_7_days}
        """

    await message.answer(stats_text)


# ===============================================================================================================


@dp.message_handler(Text(equals="User list"), state=AdminMode.admin_menu)
async def user_list_handler(message: types.Message):
    users = user_db.get_all_users_by_balance()
    if not users:
        message_response = f"*[ERROR]:* _No users found in the database..._"
        await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN)
        return

    user_list_text = "📊 User List 📊\n\n"
    for user in users:
        telegram_id, balance = user
        user_list_text += f"🔹 `{telegram_id}` : {balance}$\n"

    await message.answer(user_list_text, parse_mode=types.ParseMode.MARKDOWN)

