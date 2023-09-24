import asyncio

import httpx

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.utils.Estimate import Estimate


@dp.message_handler(Text(equals=["⛽️ Check GWEI"]), state=UserFollowing.choose_point)
async def check_gwei(message: types.Message):

    wait_message = await message.answer("⏳ Getting information about GWEI ...")

    current_gwei = Estimate.get_current_gas()

    if current_gwei >= 20:
        reply_message = f"⛽️ GWEI now: *{current_gwei}* - Fuck it, waitin' for lower gas, go touch the grass 🏡"
    else:
        reply_message = f"⛽️ GWEI now: *{current_gwei}* - perfect to make some Zora accs"

    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await bot.delete_message(chat_id=wait_message.chat.id,
                             message_id=wait_message.message_id)
    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=reply_markup)
