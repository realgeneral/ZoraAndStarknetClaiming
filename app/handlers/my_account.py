import asyncio
import string
from random import random, choice

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.create_bot import dp, bot
from app.handlers.start_cmd import user_db
from app.states import UserFollowing


@dp.message_handler(Text(equals=["🏦 My account"]), state=UserFollowing.choose_point)
async def my_account(message: types.Message):
    username = message.from_user.first_name
    telegram_id = message.from_user.id

    max_wallet_count = user_db.get_max_wallets(telegram_id)
    if max_wallet_count is not None:
        max_wallet_count = f"{max_wallet_count}"
    else:
        max_wallet_count = "Not available"

    current_balance = round(user_db.get_current_balance(telegram_id), 4)
    print(current_balance)
    if current_balance is not None:
        current_balance = f"{current_balance}$"
    else:
        max_wallet_count = "Not available"

    account_info = f" 🔹 *User:* {username} \n" \
                   f"🔹 *Telegram ID:* `{telegram_id}` \n" \
                   f"🔹 *Max wallets:* _{max_wallet_count}_ \n" \
                   f"🔹 *Balance:* _{current_balance}_ \n"

    keyboard = InlineKeyboardMarkup()
    deposit_btn = InlineKeyboardButton("👝 Deposit balance", callback_data="deposit_balance")
    keyboard.add(deposit_btn)

    await message.answer(account_info, reply_markup=keyboard, parse_mode=types.ParseMode.MARKDOWN)
