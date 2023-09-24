from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp
from app.states import UserFollowing
from app.utils.Bridger import Bridger


@dp.message_handler(Text(equals=["⬅ Go to menu", "/restart"]), state='*')
async def go_menu(message: types.Message, state: FSMContext):
    random_amount = []

    current_state = await state.get_state()

    if current_state == UserFollowing.tap_to_earn.state:
        await state.update_data(stop_flag=True)

    data = await state.get_data()
    private_keys = data.get("private_keys")
    bridge_amount = data.get("random_amount")

    if private_keys is None:
        private_keys = ["-"]
        await state.update_data(private_keys=private_keys)

        for _ in private_keys:
            random_amount.append(Bridger.choose_random_amount(0.009501, 0.01003))
        await state.update_data(random_amount=random_amount)

    if bridge_amount is None and len(random_amount) == 0:
        for _ in private_keys:
            random_amount.append(Bridger.choose_random_amount(0.009501, 0.01003))
        await state.update_data(random_amount=random_amount)

    await UserFollowing.wallet_menu.set()
    await send_menu(message)


@dp.message_handler(state=UserFollowing.wallet_menu)
async def send_menu(message: types.Message):

    message_response = "🫡 Waiting for your instructions...\n " \
                        "🔽 Choose the button below 🔽"

    # b1 = KeyboardButton("👝 Check balance")
    b2 = KeyboardButton("⛽️ Check GWEI")
    b3 = KeyboardButton("💸 Start script")
    b4 = KeyboardButton("➕ Load new wallets")
    # b5 = KeyboardButton("🔑 Check keys")
    b6 = KeyboardButton("ℹ️ FAQ")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.row(b3).row(b2, b4).row(b6)

    await UserFollowing.choose_point.set()
    await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=buttons)


