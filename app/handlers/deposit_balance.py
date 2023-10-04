import asyncio
import string
from random import random, choice

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.create_bot import dp, bot
from app.handlers.main_menu import send_menu
from app.handlers.start_cmd import user_db
from app.states import UserFollowing
from app.utils.Estimate import Estimate
from app.utils.Payments import Payments
from app.utils.PaymentSession import PaymentSession

payment_session = PaymentSession()


@dp.callback_query_handler(lambda c: c.data == "stop_deposit", state=UserFollowing.create_session)
async def stop_deposit(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id, message_id)

    callback_query.message.from_user.id = callback_query.from_user.id

    await state.update_data(stop_session=True)
    await UserFollowing.wallet_menu.set()
    await send_menu(callback_query.message, state)
    return


@dp.callback_query_handler(lambda c: c.data == "deposit_balance", state=UserFollowing.choose_point)
async def dep_balance(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)  # Это закроет уведомление "часики" на кнопке

    # Удаление предыдущего сообщения
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id, message_id)

    user_id = callback_query.from_user.id

    buttons = [
        InlineKeyboardButton("5$", callback_data="deposit_5"),
        InlineKeyboardButton("10$", callback_data="deposit_10"),
        InlineKeyboardButton("25$", callback_data="deposit_25"),
        InlineKeyboardButton("50$", callback_data="deposit_50"),
        InlineKeyboardButton("100$", callback_data="deposit_100"),
        InlineKeyboardButton("250$", callback_data="deposit_250"),
        InlineKeyboardButton("500$", callback_data="deposit_500"),
        InlineKeyboardButton("1000$", callback_data="deposit_1000"),
    ]

    keyboard = InlineKeyboardMarkup(row_width=4)

    for button in buttons:
        keyboard.insert(button)

    keyboard.insert(InlineKeyboardButton("🛑 Exit deposit session", callback_data="deposit_0"))

    await UserFollowing.create_session.set()

    await bot.send_message(user_id, f"<b>Starting deposit session</b>",
                           parse_mode=types.ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    await bot.send_message(user_id, f"Here you replenish bot balance, from where we will debit money for our services. "
                                    f"The balance is displayed in the <b>🏦 My account</b> section \n\n"
                                    f"⚠️ You will need to additionally top up your wallets, which you will use for "
                                    f"running in our service, "
                                    f" by yourself with the required amount.\n\n"
                                    f" More details are in the section <b>💸 Start script</b>",
                           parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith('deposit_'), state=UserFollowing.create_session)
async def process_deposit_callback(callback_query: types.CallbackQuery, state: FSMContext):
    deposit_amount = int(callback_query.data.split('_')[1])

    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id, message_id)

    if deposit_amount == 0:
        callback_query.message.from_user.id = callback_query.from_user.id
        await UserFollowing.wallet_menu.set()
        await send_menu(callback_query.message, state)
        return

    address, pk, mnemonic = await Payments.generate_wallet()
    session_id = '#' + ''.join(choice(string.ascii_letters + string.digits) for _ in range(5))

    await bot.answer_callback_query(callback_query.id,
                                    text=f"You have chosen to deposit {deposit_amount} USD, please wait")

    button = InlineKeyboardButton("⛔️ Close session", callback_data="stop_deposit")
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.insert(button)

    await bot.send_message(callback_query.from_user.id,
                           f"*Charge {session_id} created for 20 minutes* \n\n"
                           "You can deposit (be careful, deposit of any other asset will be lost): "
                           "USDT, USDC in Polygon or Arbitrum\n\n"
                           "*Send*\n"
                           f"*{deposit_amount}* *$USDT* or *$USDC* in Polygon or Arbitrum network\n\n"
                           f"To this address: `{address}`\n\n"
                           f"_As soon as the payment is approved you will receive a notification and the amount will be "
                           f"credited to your account_", parse_mode=types.ParseMode.MARKDOWN,
                           reply_markup=keyboard)

    payment = Payments()
    result = False
    network = '_'
    await state.update_data(stop_session=False)
    payment_session.add_session(session_id, address, pk, mnemonic, network, callback_query.from_user.id,
                                deposit_amount, 0)
    for _ in range(240):
        await asyncio.sleep(5)
        result, network = await payment.start_payment_session(deposit_amount, address)

        user_data = await state.get_data()
        if user_data.get("stop_session"):
            return

    if result:
        user_db.update_balance(callback_query.from_user.id, deposit_amount)
        payment_session.update_status_and_network(callback_query.from_user.id, 1, network)

        buttons = [
            KeyboardButton(text="⬅ Go to menu"),
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                           resize_keyboard=True)

        await bot.send_message(callback_query.from_user.id,
                               f"🎉 *Your funds have been successfully credited!*\n\n"
                               f"💰 **Balance:** {user_db.get_current_balance(callback_query.from_user.id)}$",
                               parse_mode=types.ParseMode.MARKDOWN,
                               reply_markup=reply_markup)
    else:
        buttons = [
            KeyboardButton(text="⬅ Go to menu"),
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                           resize_keyboard=True)

        await bot.send_message(callback_query.from_user.id,
                               f"⏰ *Payment Session Expired*\n\n"
                               f"_Your payment session has timed out before we could detect a deposit. "
                               f"Please contact our support team for assistance._",
                               parse_mode=types.ParseMode.MARKDOWN,
                               reply_markup=reply_markup)
