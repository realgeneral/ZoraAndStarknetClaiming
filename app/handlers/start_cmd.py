import asyncio

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.keyboards import check_sub_menu
from app.handlers import admin
from app.utils.Bridger import Bridger
from app.utils.Estimate import Estimate

CHANNEL_ID = -1001984019900
NOTSUB_MESSAGE = "Looks like you're not subscribed yet! 🙁 Subscribe now to access all the features"


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    if int(message.from_user.id) in admin.list_of_prem_users:
        max_count = 15
    else:
        max_count = 5

    await UserFollowing.check_subscribe.set()
    await message.answer(f"Welcome, <b> {message.from_user.first_name}</b>! \n\n"
                         f"The total amount of wallets you can run Zora bot: <b>{max_count}</b>\n\n"
                         "<b>⬇️ Load-up your private keys below </b>"
                         "[<a href='https://support.metamask.io/hc/en-us/articles/360015289632-How-to-export-an-account-s-private-key'>"
                         "<b>guide</b></a>]\n\n"
                         "<b>Example:</b>\n"
                         "<i>a692b7245354c12ca7ef7138bfdc040abc7d07612c9f3770c9be81d9459911ca</i>\n"
                         "<i>8cd22cacf476cd9ffebbbe05877c9cab695c6abafcad010a0194dbb1cb6e66f1</i>\n"
                         "<i>0b77a1a6618f75360f318e859a89ba8008b8d0ceb10294418443dc8fd643e6bb</i>\n\n"
                         "<b> ⚠️Please note: We do not store your data. The bot uses one-time sessions.</b>\n\n"
                         "[<a href='https://t.me/whatheshark'>Our GitHub</a>]",
                         parse_mode=types.ParseMode.HTML, reply_markup=ReplyKeyboardRemove())


def check_sub_channel(chat_member):
    if chat_member["status"] != "left":
        return True
    return False


@dp.message_handler(state=UserFollowing.check_subscribe)
async def check_subscribe(message: types.Message, state: FSMContext):
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        await UserFollowing.get_private_keys.set()
        await private_keys(message, state)
    else:
        await state.update_data(message=message)
        await UserFollowing.check_subscribe.set()
        await message.answer(
            "👋📢 Haven't joined our <a href='https://t.me/EBSH_WEB3'>channel</a> yet? \n\n"
            "We're dropping <b> crypto wisdom </b> and sharing our <b> know-how </b>. \n"
            "Your sub supports us to make <b> new retro-bots </b> for You! \n \n"
            "Hit that sub button below ⬇️, then <b> hit us back </b> with  <b> 'Done'</b>! ",
            parse_mode=types.ParseMode.HTML,
            reply_markup=check_sub_menu)


@dp.callback_query_handler(text="is_subscribe", state=UserFollowing.check_subscribe)
async def is_subscribe(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback_query.from_user.id)):
        data = await state.get_data()
        message = data.get("message")

        await UserFollowing.get_private_keys.set()
        await private_keys(message, state)

    else:
        await bot.send_message(callback_query.from_user.id, NOTSUB_MESSAGE, reply_markup=check_sub_menu)


@dp.message_handler(state=UserFollowing.get_private_keys)
async def private_keys(message: types.Message, state: FSMContext):
    random_amount = []
    message_response = ""

    private_keys = message.text.split('\n')

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    wait_message = await message.answer("⏳ Getting information about wallets ...")

    if int(message.from_user.id) in admin.list_of_prem_users:
        private_keys = private_keys[:50]
        max_count = 15
    else:
        private_keys = private_keys[:10]
        max_count = 5

    for _ in private_keys:
        random_amount.append(Bridger.choose_random_amount(0.009501, 0.01003))

    await state.update_data(private_keys=private_keys)
    await state.update_data(random_amount=random_amount)

    if len(private_keys) == 1:
        message_response += f"Wallet is successfully loaded! (max. {max_count})\n\n"
    else:
        message_response += f"<b>{len(private_keys)}</b> wallets are successfully loaded! (max. {max_count})\n\n"

    count_ok_wallet = 0

    for i, random in zip(range(len(private_keys)), random_amount):
        es = Estimate(private_keys[i])
        eth_balance = es.get_eth_balance()

        message_response += f"{i + 1}. <b>{es.get_eth_address()}</b> "

        await asyncio.sleep(1)
        is_used_bridge = await Bridger.used_bridge(private_keys[i])
        if is_used_bridge:
            message_response += f"<b>[BRIDGED]</b> (Balance in Zora: {eth_balance} ETH) ✅\n"
            count_ok_wallet += 1
        else:
            eth_required = es.eth_required(random)
            message_response += f"\n({eth_balance} ETH / {eth_required} ETH required)"

            if eth_balance != "-":
                if eth_balance >= eth_required:
                    message_response += " ✅\n"
                    count_ok_wallet += 1
                else:
                    message_response += " ❌\n"

        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Getting information about wallets {i + 1}/{len(private_keys)}")

    if count_ok_wallet == len(private_keys):
        is_ready_to_start = 1
    else:
        is_ready_to_start = 0
        message_response += f"\nPlease, deposit ETH amount on your wallet in <b>Ethereum Mainnet Chain</b> \n\n" \
                            f"* <i>Withdrawal takes ~ 5 minutes</i>\n\n "
        message_response += "<b>⚠️ Be sure to use CEX or you'll link your wallets and become sybil</b>"

    await state.update_data(is_ready_to_start=is_ready_to_start)
    await bot.delete_message(chat_id=wait_message.chat.id,
                             message_id=wait_message.message_id)

    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
        KeyboardButton(text="ℹ️ FAQ"),
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await UserFollowing.wallet_menu.set(),
    await message.answer(message_response,
                         parse_mode=types.ParseMode.HTML,
                         reply_markup=reply_markup)
