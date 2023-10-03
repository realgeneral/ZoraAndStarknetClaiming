import datetime

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

from app.create_bot import dp
from app.states import AdminMode
from app.handlers.start_cmd import user_db


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
        # b5 = KeyboardButton("Сonfig settings")
        b6 = KeyboardButton("Give money")
        b5 = KeyboardButton("⬅ Go to menu")

        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.row(b1).row(b2, b4).row(b6, b3).row(b5)

        await AdminMode.admin_menu.set()
        await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN, reply_markup=buttons)


# =================================================GIVE MONEY================================================

@dp.message_handler(Text(equals="Give money"), state=AdminMode.admin_menu)
async def send_money_to_user(message: types.Message):
    message_response = "Send user telegream_id:addind_usd"

    await AdminMode.add_money.set()
    await message.answer(message_response, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=AdminMode.add_money)
async def save_user_money(message: types.Message):
    telegram_id, money_usdt = message.text.split(':')

    try:
        user_db.update_balance(telegram_id, float(money_usdt))
        message_response = f"To `{telegram_id}` added {money_usdt}$"
    except Exception as err_:
        message_response = f"Not added: {err_}"

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
    message_response = "Send user telegream_id"

    await AdminMode.add_user.set()
    await message.answer(message_response, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=AdminMode.add_user)
async def save_prem_user(message: types.Message):
    telegram_id = message.text
    try:
        user_db.set_max_wallets_count(telegram_id, 15)
        message_response = "Saved"
    except Exception as err_:
        message_response = f"Not saved: {err_}"

    buttons = [
        KeyboardButton(text="⬅ Go to admin menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    await AdminMode.admin_menu.set()
    await message.answer(message_response, reply_markup=reply_markup)


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
        reply_message = "Today no logs"

    await message.answer(reply_message[-4000:])


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
        await message.answer("No users found in the database.")
        return

    user_list_text = "📊 User List 📊\n\n"
    for user in users:

        telegram_id, balance = user
        user_list_text += f"🔹 `{telegram_id}` : {balance}$\n"

    await message.answer(user_list_text, parse_mode=types.ParseMode.MARKDOWN)
