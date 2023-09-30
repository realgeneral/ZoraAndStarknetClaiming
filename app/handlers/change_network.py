import asyncio

import httpx

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text

from app.create_bot import dp, bot
from app.handlers.start_cmd import user_db
from app.states import UserFollowing
from app.utils.Estimate import Estimate


@dp.message_handler(Text(equals=["⚙️ Change network"]), state=UserFollowing.choose_point)
async def change_network(message: types.Message):
    b1 = KeyboardButton(text="🔮 Zora")
    b2 = KeyboardButton(text="🎡 Starknet")
    b3 = KeyboardButton(text="⬅ Go to menu")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.row(b1, b2).row(b3)

    await UserFollowing.check_claim_net.set()
    await message.answer(f"<b>⬇️ Choose network ⬇️ </b>",
                         parse_mode=types.ParseMode.HTML, reply_markup=buttons)

