import asyncio

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.handlers import admin
from app.utils.Bridger import Bridger
from app.utils.Estimate import Estimate
from app.handlers.start_cmd import user_db


@dp.message_handler(Text(equals=["➕ Load new wallets"]), state=UserFollowing.choose_point)
async def new_private_keys(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_network = data.get("current_network")
    pk_example = '-'

    if current_network == "zora":

        pk_example = "<i>private_key_of_your_wallet_1</i>\n" \
                     "<i>private_key_of_your_wallet_2</i>\n\n"

        await state.update_data(current_network=current_network)
    elif current_network == "stark":

        await state.update_data(current_network=current_network)
        pk_example = "<i>address_of_your wallet_1:private_key_of_your wallet_1</i>\n" \
                     "<i>address_of_your wallet_2:private_key_of_your wallet_2</i>\n\n"

    max_count = user_db.get_max_wallets(user_id=message.from_user.id)

    await UserFollowing.check_subscribe.set()
    await message.answer(f"{message.text[0]} The total amount of wallets you can run: <b>{max_count}</b>\n\n",
                         parse_mode=types.ParseMode.HTML, reply_markup=ReplyKeyboardRemove())

    keyboard = InlineKeyboardMarkup()
    btn_how_to = InlineKeyboardButton("🤔 How to do that?", callback_data="send_gif")
    btn_pk_info = InlineKeyboardButton("👀 Why do you need my private key?", callback_data="send_pk_info")
    keyboard.add(btn_how_to).add(btn_pk_info)

    await message.answer(f"<b>⬇️ Load-up your private keys below </b>\n\n"
                         "<b>Example:</b>\n"
                         f"{pk_example}"
                         "<b> ⚠️ Please note: We do not store your data. The bot uses one-time sessions.</b>\n\n",
                         parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
