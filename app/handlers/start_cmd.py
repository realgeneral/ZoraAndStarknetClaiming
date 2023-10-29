import asyncio
import os
from datetime import date, datetime

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup, CallbackQuery, InputFile
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.keyboards import check_sub_menu
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

    user_db.add_user(user_id, formatted_date, 1)

    buttons = [
        KeyboardButton(text="🔮 Zora"),
        KeyboardButton(text="🎡 Starknet"),
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await UserFollowing.check_claim_net.set()
    await message.answer(f"Hi, <b> {message.from_user.first_name}</b>! \n\n"
                         "<b>⬇️ Pick the project you want to do:</b>",
                         parse_mode=types.ParseMode.HTML, reply_markup=reply_markup)


@dp.message_handler(state=UserFollowing.check_claim_net)
async def check_claim_net(message: types.Message, state: FSMContext):
    if message.text.strip().lower()[2:] != "zora" and message.text.strip().lower()[2:] != "starknet":
        await message.answer(f"<b>⬇️ Choose network </b>",
                             parse_mode=types.ParseMode.HTML)
        return
    pk_example = '-'
    max_count = user_db.get_max_wallets(user_id=message.from_user.id)

    if message.text == "🔮 Zora":
        current_network = "zora"
        pk_example = "<i>private_key_of_your_wallet_1</i>\n" \
                     "<i>private_key_of_your_wallet_2</i>\n\n"

        reply_message = f"🔮 The total amount of wallets you can run: <b>{max_count}</b>\n\n"
        reply_message += f"<b>🔮 Zora script includes:</b>\n\n"
        reply_message += "       🔸 <i>Touching Zora's official bridge</i>\n" \
                         "       🔸 <i>Create own NFTs</i>\n" \
                         "       🔸 <i>Mint important NFTs (updated list)</i>\n" \
                         "       🔸 <i>Wallet warm-up (simulation of real human actions)</i>\n" \
                         "       🔸 <i>GWEI downgrade mode - literally lowers the fees to zero</i>\n\n"

        await message.answer(reply_message,
                             parse_mode=types.ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
        await state.update_data(current_network=current_network)

    elif message.text == "🎡 Starknet":
        current_network = "stark"
        pk_example = "<i>address_of_your wallet_1:private_key_of_your wallet_1</i>\n" \
                     "<i>address_of_your wallet_2:private_key_of_your wallet_2</i>\n\n"

        reply_message = f"🎡 The total amount of wallets you can run: <b>{max_count}</b>\n\n"
        reply_message += f"<b>🎡 Starknet script includes: </b>\n\n" \
                        f"<b>Interaction with dexes: </b>\n" \
                        "       🔸 <i>JediSwap ( Swaps; Liquidity Adding)</i>\n" \
                        "       🔸 <i>AvnuFi (Swaps)</i>\n" \
                        "       🔸 <i>10K Swap (Swaps)</i>\n" \
                        "       🔸 <i>Dmail (Message sender)</i>\n\n" \
                        f"<b>NFT mint : </b>\n" \
                        "       🔸 <i>StarkNetID NFT</i>\n" \
                        "       🔸 <i>StarkVerse NFT</i>\n\n"
        await message.answer(reply_message,
                             parse_mode=types.ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
        await state.update_data(current_network=current_network)

    await UserFollowing.check_subscribe.set()

    keyboard = InlineKeyboardMarkup()
    btn_how_to = InlineKeyboardButton("🤔 How to do that?", callback_data="send_gif")
    btn_pk_info = InlineKeyboardButton("👀 Why do you need my private key?", callback_data="send_pk_info")
    keyboard.add(btn_how_to).add(btn_pk_info)

    await message.answer(f"<b>{message.text[0]}️ Load-up your private keys below </b>\n\n"
                         "<b>Example:</b>\n"
                         f"{pk_example}"
                         "<b> ⚠️ Please note: We do not store your data. The bot uses one-time sessions.</b>\n\n",
                         parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'send_gif', state=UserFollowing.check_subscribe)
async def send_gif(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_network = data.get("current_network")

    if current_network == 'zora':
        metamask_video_path = "app/data/metamask.mp4"
        await bot.send_animation(callback_query.from_user.id, InputFile(metamask_video_path), caption="🦊 Metamask")
    if current_network == 'stark':
        gif_path = "app/data/argentx.mp4"
        await bot.send_animation(callback_query.from_user.id, InputFile(gif_path), caption="🅰️rgentX")

    await bot.answer_callback_query(callback_query.id)
    await UserFollowing.check_subscribe.set()


@dp.callback_query_handler(lambda c: c.data == 'send_pk_info', state=UserFollowing.check_subscribe)
async def send_pk_info(callback_query: CallbackQuery):
    data = "At the moment there is no way to interact with the wallet (make bridges, swaps, mints, etc) without using a private key. \n\n" \
           'We guarantee you that your funds are SAFU because the bot is based on a so-called "disposable states" which means that during it\'s work no data is stored. Bot "resets the session" when all tasks are completed. \n\n' \
           "If you want to have a talk with our team and learn more about this technology feel free to contact us: @ebsh_web3_support"
    await bot.send_message(callback_query.from_user.id, data)
    await bot.answer_callback_query(callback_query.id)
    await UserFollowing.check_subscribe.set()


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
    is_ready_to_start = 0

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
            else:
                keys_dict[counter_pk] = None

        await state.update_data(private_keys=keys_dict)

        for i in range(len(keys_dict)):
            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Getting information about wallets {i + 1}/{len(keys_dict)}")

            message_response += f"Wallet <b>#{i + 1}</b>"
            if keys_dict[i + 1] is None:
                is_be_invalid = True
                message_response += f" <i>[INVALID FORMAT]</i> ❌\n"
                continue
            else:

                try:
                    cl = ClientHelper(keys_dict[i + 1][1],
                                      keys_dict[i + 1][0],
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
        is_ready_to_start = 1

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
                eth_required = 0.015

                message_response += f"\n({eth_balance} ETH / {eth_required} ETH required)"

                if eth_balance != "-":
                    if eth_balance >= eth_required:
                        message_response += " ✅\n"
                        count_ok_wallet += 1
                        print("eth_balance >= eth_required")
                    else:
                        print("eth_balance < eth_required")
                        count_ok_wallet += 1
                        message_response += " ❌\n"
                elif eth_balance == "-":
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

    if not is_be_invalid and is_ready_to_start:
        if len(list_private_keys) == 1:
            message_response += f"\n\nWallet is successfully loaded! (max. {max_count})\n\n"
        else:
            message_response += f"<b>{len(list_private_keys)}</b> wallets are successfully loaded! (max. {max_count})\n\n"

        await UserFollowing.choose_route.set()

        if current_network == 'zora':
            keyboard = InlineKeyboardMarkup()
            btn_warm = InlineKeyboardButton("Warming Up", callback_data="earn_zora_warm")
            btn_main = InlineKeyboardButton("Main route", callback_data="earn_zora_main")
            keyboard.add(btn_warm).add(btn_main)

            await message.answer("<b>🔮 Change the route to run: </b>",
                                 parse_mode=types.ParseMode.HTML,
                                 reply_markup=keyboard)

        if current_network == 'stark':
            btn_warm = InlineKeyboardButton("Warming Up", callback_data="earn_stark_warm")
            btn_main = InlineKeyboardButton("Main route", callback_data="earn_stark_main")
            keyboard.add(btn_warm).add(btn_main)

            await message.answer("<b>🎡 Change the route to run: </b>",
                                 parse_mode=types.ParseMode.HTML,
                                 reply_markup=keyboard)
        return
    else:

        if not is_ready_to_start:
            message_response += f"\n😕 You don't have required amount ETH on your wallet\n"
        else:
            message_response += f"\n😕 Invalid private keys\n"

        await UserFollowing.get_private_keys.set()
        await message.answer(message_response, parse_mode=types.ParseMode.HTML)
        return


@dp.callback_query_handler(lambda query: query.data.startswith('earn'), state=UserFollowing.choose_route)
async def choose_route(callback_query: types.CallbackQuery, state: FSMContext):
    current_network = callback_query.data.split('_')[1]
    run_type = callback_query.data.split('_')[2]

    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id, message_id)
    await bot.answer_callback_query(callback_query.id,
                                    text=f"You have chosen {run_type} in {current_network}")

    is_free_run = user_db.is_free_run(callback_query.from_user.id)  # 1 == free

    if current_network == "zora":
        if run_type == "main":
            if is_free_run == 1:
                await state.update_data(is_ready=0)
                await state.update_data(stop_flag=False)

                from app.handlers.zora_autopilot import start_earn

                await state.update_data(is_main_zora=1)
                await UserFollowing.tap_to_earn.set()
                await start_earn(message, state)
                return
            else:
                await state.update_data(is_main_zora=1)
        elif run_type == "warm":
            if is_free_run == 1:
                await state.update_data(is_ready=0)
                await state.update_data(stop_flag=False)

                from app.handlers.zora_autopilot import start_earn

                await state.update_data(is_warm_zora=1)
                await UserFollowing.tap_to_earn.set()
                await start_earn(message, state)
                return
            else:
                await state.update_data(is_warm_zora=1)
    elif current_network == "stark":
        if run_type == "main":
            if is_free_run == 1:
                await state.update_data(is_ready=0)
                await state.update_data(stop_flag=False)

                from app.handlers.stark_autopilot import start_earn_stark

                await state.update_data(is_main_stark=1)
                await UserFollowing.tap_to_earn_stark.set()
                await start_earn_stark(message, state)
                return
            else:
                await state.update_data(is_main_stark=1)
        elif run_type == "warm":
            if is_free_run == 1:
                await state.update_data(is_ready=0)
                await state.update_data(stop_flag=False)

                from app.handlers.stark_autopilot import start_earn_stark

                await state.update_data(is_warm_stark=1)
                await UserFollowing.tap_to_earn_stark.set()
                await start_earn_stark(message, state)
                return
            else:
                await state.update_data(is_warm_stark=1)

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
