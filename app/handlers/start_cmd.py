import asyncio
from datetime import date, datetime

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.keyboards import check_sub_menu
from app.handlers.zora_autopilot import start_earn
from app.handlers.stark_autopilot import start_earn_stark
from app.utils.Bridger import Bridger
from app.utils.Estimate import Estimate
from app.utils.UsersDb import Users
from app.utils.stark_utils.Client import ClientHelper


CHANNEL_ID = -1001984019900
NOTSUB_MESSAGE = "Looks like you're not subscribed yet! 🙁 Subscribe now to access all the features"

user_db = Users()


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    user_db.add_user(user_id, formatted_date, wallet_count=1)

    buttons = [
        KeyboardButton(text="🔮 Zora"),
        KeyboardButton(text="🎡 Starknet"),
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await UserFollowing.check_claim_net.set()
    await message.answer(f"Hi, <b> {message.from_user.first_name}</b>! \n\n"
                         "<b>⬇️Pick the project you want to do:</b>",
                         parse_mode=types.ParseMode.HTML, reply_markup=reply_markup)


@dp.message_handler(state=UserFollowing.check_claim_net)
async def check_claim_net(message: types.Message, state: FSMContext):
    if message.text.strip().lower()[2:] != "zora" and message.text.strip().lower()[2:] != "starknet":
        await message.answer(f"<b>⬇️ Choose network </b>",
                             parse_mode=types.ParseMode.HTML)
        return
    pk_example = '-'

    if message.text == "🔮 Zora":
        current_network = "zora"
        pk_example = "<i>a692b7245354c12ca7ef7138bfdc040abc7d07612c9f3770c9be81d9459911ca</i>\n" \
                     "<i>8cd22cacf476cd9ffebbbe05877c9cab695c6abafcad010a0194dbb1cb6e66f1</i>\n" \
                     "<i>0b77a1a6618f75360f318e859a89ba8008b8d0ceb10294418443dc8fd643e6bb</i>\n\n"
        await state.update_data(current_network=current_network)
    elif message.text == "🎡 Starknet":
        current_network = "stark"
        await state.update_data(current_network=current_network)
        pk_example = "<i>STARKNET_WALLET_ADDRESS:STARKNET_PRIVATE_KEY</i>\n" \
                     "<i>STARKNET_WALLET_ADDRESS:STARKNET_PRIVATE_KEY</i>\n\n"

    max_count = user_db.get_max_wallets(user_id=message.from_user.id)

    await UserFollowing.check_subscribe.set()
    await message.answer(f"{message.text[0]} The total amount of wallets you can run: <b>{max_count}</b>\n\n"
                         "<b>⬇️ Load-up your private keys below </b>"
                         "[<a href='https://support.metamask.io/hc/en-us/articles/360015289632-How-to-export-an-account-s-private-key'>"
                         "<b>guide</b></a>]\n\n"
                         "<b>Example:</b>\n"
                         f"{pk_example}"
                         "<b> ⚠️Please note: We do not store your data. The bot uses one-time sessions.</b>\n\n",
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
    max_count = user_db.get_max_wallets(user_id=message.from_user.id)
    is_free_run = user_db.is_free_run(message.from_user.id)  # 1 == free

    message_response = ""
    is_be_invalid = False

    lines = message.text.strip().split("\n")
    list_private_keys = lines[:max_count]

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    wait_message = await message.answer("⏳ Getting information about wallets ...")


    data = await state.get_data()
    current_network = data.get("current_network")

    if current_network == 'stark':
        keys_dict = {}
        counter_pk = 0

        for line in list_private_keys:
            counter_pk += 1
            if ":" in line:
                stark_wallet_address, starknet_key = line.split(":")
                keys_dict[counter_pk] = [stark_wallet_address, starknet_key]
                print(keys_dict)
            else:
                keys_dict[counter_pk] = None

        await state.update_data(private_keys=keys_dict)

        for i in range(len(keys_dict)):
            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Getting information about wallets {i + 1}/{len(keys_dict)}")

            message_response += f"Wallet <b>#{i + 1}</b>"
            if keys_dict[i+1] is None:
                is_be_invalid = True
                message_response += f" <i>[INVALID FORMAT]</i> ❌\n"
                continue
            else:

                try:
                    cl = ClientHelper(keys_dict[i+1][1],
                                      keys_dict[i+1][0],
                                      "https://starknet-mainnet.infura.io/v3/7eec932e2c324e20ac051e0aa3741d9f")

                    balance_in_stark = await cl.get_balance()
                    # balance_in_stark = 0
                    if balance_in_stark == 0:
                        message_response += f" <i>[Balance {round(balance_in_stark, 1)} ETH]</i> ❌\n"
                    else:
                        message_response += f" <i>[Balance {round(balance_in_stark, 5)} ETH]</i> ✅\n"
                except Exception:
                    is_be_invalid = True
                    message_response += f" <i>[INVALID FORMAT]</i> ❌\n"

    if current_network == 'zora':

        await state.update_data(private_keys=list_private_keys)

        random_amount = []
        for _ in list_private_keys:
            random_amount.append(Bridger.choose_random_amount(0.009501, 0.01003))
            await state.update_data(random_amount=random_amount)

        count_ok_wallet = 0
        for i, random in zip(range(len(list_private_keys)), random_amount):
            es = Estimate(list_private_keys[i])
            eth_balance = es.get_eth_balance()

            message_response += f"{i + 1}. <b>{es.get_eth_address()}</b> "

            await asyncio.sleep(1)

            is_used_bridge = await Bridger.used_bridge(list_private_keys[i])
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
                        is_be_invalid = True
                        message_response += " ❌\n"
                else:
                    is_be_invalid = True

            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Getting information about wallets {i + 1}/{len(list_private_keys)}")

        if count_ok_wallet == len(list_private_keys):
            is_ready_to_start = 1
        else:
            is_ready_to_start = 0
            message_response += f"\nPlease, deposit ETH amount on your wallet in <b>Ethereum Mainnet Chain</b> \n\n" \
                                f"* <i>Withdrawal takes ~ 5 minutes</i>\n\n "
            message_response += "<b>⚠️ Be sure to use CEX or you'll link your wallets and become sybil</b>\n\n"

        await state.update_data(is_ready_to_start=is_ready_to_start)  # если на кошельках достаточно ETH для бриджа

    await bot.delete_message(chat_id=wait_message.chat.id,
                             message_id=wait_message.message_id)

    if not is_be_invalid:
        if len(list_private_keys) == 1:
            message_response += f"\n\nWallet is successfully loaded! (max. {max_count})\n\n"
        else:
            message_response += f"<b>{len(list_private_keys)}</b> wallets are successfully loaded! (max. {max_count})\n\n"

        if is_free_run == 1:
            if current_network == 'zora':
                await UserFollowing.get_private_keys.set()
                await start_earn_stark(message, state)
                return
            if current_network == 'stark':
                await UserFollowing.tap_to_earn_stark.set()
                await start_earn(message, state)
                return

    else:
        message_response += f"\n\n☹️ TRY ONE MORE\n\n"

        await UserFollowing.tap_to_earn.set()
        await message.answer(message_response, parse_mode=types.ParseMode.HTML)
        return
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
