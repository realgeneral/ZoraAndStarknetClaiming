import asyncio
import random
from dataclasses import dataclass

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.handlers.start_cmd import user_db
from app.create_bot import dp, bot
from app.states import UserFollowing

from app.logs import logging as logger
from app.utils.Randomiser import Randomiser
from app.utils.configs.animals import animals
from app.utils.defi.AvnuFi import AvnuFi
from app.utils.defi.Dmail import Dmail
from app.utils.defi.JediSwap import JediSwap
from app.utils.defi.TenkSwap import TenkSwap
from app.utils.mint.StarkMinter import Minter as Stark_Minter
from app.utils.stark_utils.Client import Client
from app.handlers.admin import get_one_wallet_run_price




@dataclass
class RunningParams:
    STARKNET_RPC: str = "https://starknet-mainnet.infura.io/v3/7eec932e2c324e20ac051e0aa3741d9f"
    SWAP_SLIPPAGE: int = 2
    RANDOM_DELAY: int = random.randint(30, 60)
    JEDISWAP_SWAP_COUNT: int = None
    JEDISWAP_LP_COUNT: int = None
    AVNUFI_SWAP_COUNT: int = None
    TENKSWAP_SWAP_COUNT: int = None
    STARKVERSE_NFT_MINT_COUNT: int = random.randint(1, 3)
    STARKNETID_NFT_MINT_COUNT: int = random.randint(1, 3)
    JEDISWAP_SWAP_PERCENTAGE: int = random.randint(50, 70)
    JEDISWAP_LIQ_PERCENTAGE: int = random.randint(60, 80)
    AVNUFI_SWAP_PERCENTAGE: int = random.randint(50, 70)
    TENK_SWAP_PERCENTAGE: int = random.randint(50, 70)
    DMAIL_MESSAGES_COUNT: int = random.randint(10, 20)


@dp.message_handler(Text(equals="💸 Start Starknet script"), state=UserFollowing.choose_point)
async def tap_to_earn_stark(message: types.Message, state: FSMContext):
    reply_message = ""

    data = await state.get_data()
    private_keys = list(data.get("private_keys"))

    balance_in_bot = user_db.get_current_balance(message.from_user.id)
    is_free_run = user_db.is_free_run(message.from_user.id)  # 1 == free

    one_wallet_run_price = get_one_wallet_run_price()
    print(f"one_wallet_run_price stark - {one_wallet_run_price}")

    if balance_in_bot < (len(private_keys) * one_wallet_run_price) and is_free_run == 0:
        reply_message += f"*Your balance* {balance_in_bot}$ is less than required " \
                         f"({len(private_keys)} x {one_wallet_run_price} = {(len(private_keys) * one_wallet_run_price)}$) \n"

        b1 = KeyboardButton("⬅ Go to menu")

        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.row(b1)
        await message.answer(reply_message, parse_mode=types.ParseMode.MARKDOWN,
                             reply_markup=buttons)
        return

    if len(private_keys) == 1:
        edit_message = "Waiting for refilling of the wallet...."
    else:
        edit_message = "Waiting for refilling of the wallets...."

    wait_message = await message.answer(edit_message)

    await bot.edit_message_text(chat_id=wait_message.chat.id,
                                message_id=wait_message.message_id,
                                text=f"⏳ Preparing information about the script ... 0% ...")
    len_pk = len(private_keys)

    reply_message += f"\n📍 Total сount of wallets: <b>{len_pk}</b>\n\n"
    reply_message += f"<b>Bot superpower's:</b>\n\n" \
                     "       🔸 <i><a href='https://app.jediswap.xyz/#/swap'>JediSwap</a></i>\n" \
                     "       🔸 <i><a href='https://www.avnu.fi/'>AVNU</a></i>\n" \
                     "       🔸 <i><a href='https://10kswap.com/swap'>10K Swap</a></i>\n" \
                     "       🔸 <i><a href='https://dmailnetwork.gitbook.io/user_guide/starknet-user-guide'>Dmail message</a></i>\n" \
                     "       🔸 <i><a href='https://www.starknet.id/'>StarkNetIDNFT Minting</a></i>\n" \
                     "       🔸 <i><a href='https://twitter.com/Starknet_Verse'>StarkVerseNFT Minting</a></i>\n" \
                     "       🔸 <i><a href=' https://app.jediswap.xyz/#/pool'>JediSwap Liquidity Adding</a></i>\n"

    total_time = "TODO"
    reply_message += f"🕔 <b>Total time</b> ~ {total_time} hours *\n\n" \
                     f"<i>* We stretch out time to imitate how humans act</i>\n\n"
    reply_message += "To stop script, press   <b>«⛔️ Stop ⛔️»</b> "

    await bot.edit_message_text(chat_id=wait_message.chat.id,
                                message_id=wait_message.message_id,
                                text=f"⏳ Preparing information about the script ... 100% ...")

    b1 = KeyboardButton("🐳 LFG!")
    b2 = KeyboardButton("⛔️ Stop ⛔️")
    # b3 = KeyboardButton("⬅ Go to menu")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.row(b1, b2)

    await state.update_data(is_ready=0)
    await state.update_data(stop_flag=False)
    await UserFollowing.tap_to_earn_stark.set()

    await bot.delete_message(chat_id=wait_message.chat.id,
                             message_id=wait_message.message_id)
    await message.answer(reply_message, parse_mode=types.ParseMode.HTML,
                         reply_markup=buttons)


@dp.message_handler(Text(equals="⛔️ Stop ⛔️"), state=UserFollowing.tap_to_earn_stark)
async def stop_earn(message: types.Message, state: FSMContext):
    message_response = "❗️ Stopping ... \n"

    await state.update_data(stop_flag=True)

    is_ready = 0
    await state.update_data(is_ready=is_ready)

    data = await state.get_data()

    if "final_statistic_stark" in data:
        message_response += data.get("final_statistic_stark")

    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await UserFollowing.wallet_menu.set()
    await message.answer(message_response,
                         parse_mode=types.ParseMode.HTML,
                         reply_markup=reply_markup)


@dp.message_handler(Text(equals="🐳 LFG!"), state=UserFollowing.tap_to_earn_stark)
async def start_earn_stark(message: types.Message, state: FSMContext):
    data = await state.get_data()
    is_ready = data.get("is_ready")
    TOTAL_SLEEP_TIME = 0

    if is_ready == 0:

        is_ready = -1
        await state.update_data(is_ready=is_ready)
        private_keys = dict(data.get("private_keys"))

        count_keys = len(private_keys)

        final_statistic = "\n📊 <b>Statistic</b> 📊\n\n"
        current_statistic = "\n📊 <b>Statistic</b> 📊\n\n"
        await state.update_data(final_statistic_stark=current_statistic)

        wait_message = await message.answer("Starting *Starknet* script ✈️...", parse_mode=types.ParseMode.MARKDOWN)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        for i in range(count_keys):
            try:
                wallet_statistics = {
                    "JediSwap Swap": "",
                    "AvnuFi Swap": "",
                    "10kSwap Swap": "",
                    "Dmail message": "",
                    "StarkVerseNFT Minting": "",
                    "StarkNetIDNFT Minting": "",
                    "JediSwap Liquidity Adding": ""
                }

                params = RunningParams()

                client = Client(address=int(private_keys[i+1][0], 16),
                                private_key=int(private_keys[i+1][1], 16),
                                address_to_log=private_keys[i+1][0],
                                starknet_rpc=params.STARKNET_RPC,
                                MAX_GWEI=3000)

                ########################################### TASKS PREPARING #################################
                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"⏳ _Preparing tasks..._", parse_mode=types.ParseMode.MARKDOWN)

                user_data = await state.get_data()
                if user_data.get("stop_flag"):
                    return

                TASKS = []

                JediSwap_client = JediSwap(client=client, JEDISWAP_SWAP_PERCENTAGE=params.JEDISWAP_SWAP_PERCENTAGE,
                                           JEDISWAP_LIQ_PERCENTAGE=params.JEDISWAP_LIQ_PERCENTAGE,
                                           SLIPPAGE=params.SWAP_SLIPPAGE)
                AvnuFi_client = AvnuFi(client=client, AVNUFI_SWAP_PERCENTAGE=params.AVNUFI_SWAP_PERCENTAGE,
                                       SLIPPAGE=params.SWAP_SLIPPAGE)
                TenkSwap_client = TenkSwap(client=client, TENK_SWAP_PERCENTAGE=params.TENK_SWAP_PERCENTAGE,
                                           SLIPPAGE=params.SWAP_SLIPPAGE)
                Minter_client = Stark_Minter(client=client)

                Dmail_client = Dmail(client=client)

                TASKS.append(("JediSwap Swap", JediSwap_client.swap))
                TASKS.append(("AvnuFi Swap", AvnuFi_client.swap))
                TASKS.append(("10kSwap Swap", TenkSwap_client.swap))
                TASKS.append(("StarkVerseNFT Minting", Minter_client.mintStarkVerse))
                TASKS.append(("StarkNetIDNFT Minting", Minter_client.mintStarknetIdNFT))
                TASKS.append(("Dmail message", Dmail_client.send_message))

                random.shuffle(TASKS)
                # Adding liq at the end
                TASKS.append(("JediSwap Liquidity Adding", JediSwap_client.add_liquidity))

                ########################################### TASKS PERFORMING #################################

                start_delay = params.RANDOM_DELAY

                user_data = await state.get_data()
                if user_data.get("stop_flag"):
                    return

                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"⏳ *[{client.address_to_log}]* Sleeping for _{start_delay} s_ "
                                                 f"before starting script",
                                            parse_mode=types.ParseMode.MARKDOWN)

                await asyncio.sleep(start_delay)
                TOTAL_SLEEP_TIME += start_delay

                log_counter = 0

                user_data = await state.get_data()
                if user_data.get("stop_flag"):
                    return

                for task_name, task in TASKS:

                    current_statistic += f"\nWallet <b>[{client.address_to_log}]</b>\n\n"

                    user_data = await state.get_data()
                    if user_data.get("stop_flag"):
                        return

                    params = RunningParams()  # новый объект для генерации нового рандом делея
                    delay = params.RANDOM_DELAY
                    if log_counter != 0:
                        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                    message_id=wait_message.message_id,
                                                    text=f"*[{client.address_to_log}]* Sleeping for _{delay} s_ before doing next task",
                                                    parse_mode=types.ParseMode.MARKDOWN)
                        await asyncio.sleep(delay)
                        TOTAL_SLEEP_TIME += delay

                    user_data = await state.get_data()
                    if user_data.get("stop_flag"):
                        return

                    try:
                        balance = (await client.get_balance()).Ether
                        balance_to_print = round((await client.get_balance()).Ether, 5)

                        user_data = await state.get_data()
                        if user_data.get("stop_flag"):
                            return

                        if balance >= 0.000055:
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"*[{client.address_to_log}]* Performing _{task_name}_...",
                                                        parse_mode=types.ParseMode.MARKDOWN)
                            await task()
                            wallet_statistics[task_name] = "✅"

                            current_statistic += f"{task_name}: <i>✅</i>\n"
                            await state.update_data(final_statistic_stark=current_statistic)

                            log_counter = 1
                        else:

                            user_data = await state.get_data()
                            if user_data.get("stop_flag"):
                                return

                            logger.error(
                                f"[{client.address_to_log}] Insufficient funds in StarkNet. Balance: {balance_to_print} ETH")

                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"❌ *[{client.address_to_log}]* Insufficient funds. Balance: _{balance_to_print} ETH_",
                                                        parse_mode=types.ParseMode.MARKDOWN)

                            # заполнение оставшейся статистики крестиками в случае нехватки денег
                            for remaining_task_name, _ in TASKS[TASKS.index((task_name, task)):]:
                                wallet_statistics[remaining_task_name] = f"❌ Insufficient funds. Balance: {balance_to_print} ETH"
                                current_statistic += f"{remaining_task_name}: ❌ Insufficient funds. Balance: {balance_to_print} ETH\n"
                            await state.update_data(final_statistic_stark=current_statistic)

                            break
                    except Exception as err:

                        user_data = await state.get_data()
                        if user_data.get("stop_flag"):
                            return

                        if "nonce" in str(err):
                            logger.error(f"[{client.address_to_log}] Invalid transaction nonce")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"❌ *[{client.address_to_log}]* Invalid transaction nonce",
                                                        parse_mode=types.ParseMode.MARKDOWN)

                            wallet_statistics[task_name] = "❌ Invalid transaction nonce"
                            current_statistic += f"{task_name}: <i>❌ Invalid transaction nonce</i>\n"
                            await state.update_data(final_statistic_stark=current_statistic)

                        elif "Client failed with code 63" in str(err):
                            logger.error(f"[{client.address_to_log}] {err}")
                            try:
                                retry_delay = random.randint(15, 30)
                                logger.info(f"[{client.address_to_log}] Sleeping for {retry_delay} s before retrying")

                                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                            message_id=wait_message.message_id,
                                                            text=f"❌ *[{client.address_to_log}]* Sleeping for _{retry_delay} s_ before retrying",
                                                            parse_mode=types.ParseMode.MARKDOWN)

                                await asyncio.sleep(retry_delay)
                                await task()
                                wallet_statistics[task_name] = "✅"

                                current_statistic += f"{task_name}: <i>✅</i>\n"
                                await state.update_data(final_statistic_stark=current_statistic)

                            except Exception as retry_err:
                                logger.error(f"[{client.address_to_log}] Error while retrying task after 63 error: {retry_err}")
                                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                            message_id=wait_message.message_id,
                                                            text=f"❌ *[{client.address_to_log}]* Error while retrying task after 63 error: _{retry_err}_",
                                                            parse_mode=types.ParseMode.MARKDOWN)

                                wallet_statistics[task_name] = "❌ Client failed"

                                current_statistic += f"{task_name}: <i>❌ Client failed</i>\n"
                                await state.update_data(final_statistic_stark=current_statistic)
                        elif "Insufficient tokens on balance to add a liquidity pair. Only ETH is available" in str(
                                err):
                            logger.error(f"[{client.address_to_log}] {err}")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"❌ *[{client.address_to_log}]* _{err}_",
                                                        parse_mode=types.ParseMode.MARKDOWN)

                            wallet_statistics[task_name] = "❌ Insufficient tokens on balance to add a liquidity pair"

                            current_statistic += f"{task_name}: <i>❌ Insufficient tokens on balance to add a liquidity pair</i>\n"
                            await state.update_data(final_statistic_stark=current_statistic)
                        elif "host starknet-mainnet.infura.io" in str(err):
                            logger.error(f"[{client.address_to_log}] {err}")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"❌ *[{client.address_to_log}]* _{err}_",
                                                        parse_mode=types.ParseMode.MARKDOWN)
                            try:
                                user_data = await state.get_data()
                                if user_data.get("stop_flag"):
                                    return

                                retry_delay = random.randint(15, 30)

                                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                            message_id=wait_message.message_id,
                                                            text=f"*[{client.address_to_log}]* Sleeping for _{retry_delay} s_ before retrying",
                                                            parse_mode=types.ParseMode.MARKDOWN)

                                await asyncio.sleep(retry_delay)

                                user_data = await state.get_data()
                                if user_data.get("stop_flag"):
                                    return

                                TOTAL_SLEEP_TIME += retry_delay
                                await task()
                                wallet_statistics[task_name] = "✅"
                                current_statistic += f"{task_name}: <i>✅</i>\n"
                            except Exception as retry_err:
                                logger.error(
                                    f"[{client.address_to_log}] Error while retrying task after connection issue: {retry_err}")
                                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                            message_id=wait_message.message_id,
                                                            text=f"*[{client.address_to_log}]* Error while retrying task after connection issue: _{retry_err}_",
                                                           parse_mode=types.ParseMode.MARKDOWN)
                                wallet_statistics[task_name] = "❌ Lost connection with starknet-mainnet.infura.io"

                                current_statistic += f"{task_name}: <i>❌ Lost connection with starknet-mainnet.infura.io</i>\n"
                                await state.update_data(final_statistic_stark=current_statistic)

                        elif "Transaction reverted: Error in the called contract." in str(err):
                            logger.error(f"[{client.address_to_log}] {err}")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"*[{client.address_to_log}]* _Transaction reverted: Error in the called contract_",
                                                        parse_mode=types.ParseMode.MARKDOWN)

                            wallet_statistics[task_name] = "❌ Transaction reverted: Error in the called contract"

                            current_statistic += f"{task_name}: <i>❌ Transaction reverted: Error in the called contract</i>\n"
                            await state.update_data(final_statistic_stark=current_statistic)

                        else:
                            logger.error(f"[{client.address_to_log}] Error while performing task: {err}")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"*[{client.address_to_log}]* Error while performing task: _{err}_",
                                                        parse_mode=types.ParseMode.MARKDOWN)
                            wallet_statistics[task_name] = f"❌ Error while performing task: {err}"

                            current_statistic += f"{task_name}: <i>❌ Error while performing task: {err}</i>\n"
                            await state.update_data(final_statistic_stark=current_statistic)

                # формирую финальное сообщение о статистике исходя из собранной статистики одного прогнанного кошелька
                final_statistic += f"\nWallet <b>[{client.address_to_log}]</b>\n\n"

                for task_name, status in wallet_statistics.items():
                    final_statistic += f"{task_name}: <i>{status}</i>\n"

            except Exception as err:
                logger.error(f"#{i} Something went wrong while client declaring or getting params: {err}")
                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"#{i} Something went wrong while client declaring or getting params: _{err}_",
                                            parse_mode=types.ParseMode.MARKDOWN)

        is_free_run = user_db.is_free_run(message.from_user.id)  # 1 == free

        data = await state.get_data()
        private_keys = list(data.get("private_keys"))

        one_wallet_run_price = get_one_wallet_run_price()

        if is_free_run == 0:
            user_db.update_balance(message.from_user.id, -(len(private_keys) * one_wallet_run_price))

        is_ready = 0
        await state.update_data(is_ready=is_ready)
        await UserFollowing.wallet_menu.set()

        await bot.delete_message(chat_id=wait_message.chat.id,
                                 message_id=wait_message.message_id)

        buttons = [
            KeyboardButton(text="⬅ Go to menu"),
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                           resize_keyboard=True)
        await message.answer(final_statistic,
                             parse_mode=types.ParseMode.HTML,
                             reply_markup=reply_markup)

        if is_free_run == 1:
            user_db.set_false_free_run(message.from_user.id)
            congratulations = "🎉 Congratulations!  You have farmed 1 wallet on a Tier 1 Project.\n" \
                              "😤 In the past the average web3 user has made $500 for doing the same actions in air drops. "
            await message.answer(congratulations,
                                 parse_mode=types.ParseMode.HTML,
                                 reply_markup=reply_markup)

    else:
            b1 = KeyboardButton("🐳 LFG!")
            b2 = KeyboardButton("⛔️ Stop ⛔️")
            b3 = KeyboardButton("⬅ Go to menu")

            buttons = ReplyKeyboardMarkup(resize_keyboard=True)
            buttons.row(b1, b2).row(b3)

            is_ready = 0
            await state.update_data(is_ready=is_ready)
            await message.answer(f"❗️ *Wait for wallet processing*", parse_mode=types.ParseMode.MARKDOWN,
                                 reply_markup=buttons)
