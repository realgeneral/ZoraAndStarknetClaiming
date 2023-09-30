from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.utils.Bridger import Bridger


# TODO переписать под выбранные сети

@dp.message_handler(Text(equals=["⬅ Go to menu", "/restart"]), state='*')
async def go_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_network = data.get("current_network")

    current_state = await state.get_state()
    if current_state == UserFollowing.tap_to_earn.state:
        await state.update_data(stop_flag=True)

    data = await state.get_data()
    private_keys = data.get("private_keys")

    if current_network == "stark":
        if private_keys is None:
            private_keys = {1: [0, 0]}
            await state.update_data(private_keys=private_keys)

    if current_network == "zora":
        bridge_amount = data.get("random_amount")

        if private_keys is None:
            private_keys = ["-"]
            await state.update_data(private_keys=private_keys)

        random_amount = []
        for _ in private_keys:
                random_amount.append(Bridger.choose_random_amount(0.009501, 0.01003))
        await state.update_data(random_amount=random_amount)

        if bridge_amount is None and len(random_amount) == 0:
            for _ in private_keys:
                random_amount.append(Bridger.choose_random_amount(0.009501, 0.01003))
            await state.update_data(random_amount=random_amount)

    await UserFollowing.wallet_menu.set()
    await send_menu(message, state)


@dp.message_handler(state=UserFollowing.wallet_menu)
async def send_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_network = data.get("current_network")

    message_response = "🫡 Waiting for your instructions...\n " \
                       "🔽 Choose the button below 🔽"

    b1 = KeyboardButton("🏦 My account")
    b2 = KeyboardButton("⛽️ Check GWEI")
    b5 = KeyboardButton("⚙️ Change network")

    if current_network == 'zora':
        b3 = KeyboardButton("💸 Start Zora script")
    elif current_network == 'stark':
        b3 = KeyboardButton("💸 Start Starknet script")
    else:
        b3 = b5
        b5 = None

    b4 = KeyboardButton("➕ Load new wallets")
    b6 = KeyboardButton("ℹ️ FAQ")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)

    if b5:
        buttons.row(b1, b3).row(b5, b4).row(b2, b6)
    else:
        buttons.row(b1, b3).row(b4).row(b2, b6)


    await UserFollowing.choose_point.set()
    await bot.send_message(message.from_user.id, message_response,  parse_mode=types.ParseMode.MARKDOWN,
                           reply_markup=buttons)
