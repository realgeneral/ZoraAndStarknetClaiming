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
    STARKNET_RPC: str = random.choice(["https://starknet-mainnet.infura.io/v3/7eec932e2c324e20ac051e0aa3741d9f", "https://starknet-mainnet.infura.io/v3/283bed0b326d44c795ab05a8cb9811e4", "https://starknet-mainnet.infura.io/v3/d0f5cc7661554f7a92e0a781c4d8df09"])
    SWAP_SLIPPAGE: int = 2
    RANDOM_DELAY: int = random.randint(30, 60)
    JEDISWAP_SWAP_COUNT: int = random.randint(2, 5)
    JEDISWAP_LP_COUNT: int = 1
    AVNUFI_SWAP_COUNT: int = random.randint(3, 5)
    TENKSWAP_SWAP_COUNT: int = random.randint(3, 5)
    STARKVERSE_NFT_MINT_COUNT: int = random.randint(1, 3)
    STARKNETID_NFT_MINT_COUNT: int = random.randint(1, 3)
    JEDISWAP_SWAP_PERCENTAGE: int = random.randint(55, 75)
    JEDISWAP_LIQ_PERCENTAGE: int = random.randint(65, 75)
    AVNUFI_SWAP_PERCENTAGE: int = random.randint(55, 75)
    TENK_SWAP_PERCENTAGE: int = random.randint(55, 75)
    DMAIL_MESSAGES_COUNT: int = random.randint(3, 8)

    # JEDISWAP_SWAP_COUNT: int = 3
    # JEDISWAP_LP_COUNT: int = 0
    # AVNUFI_SWAP_COUNT: int = 2
    # TENKSWAP_SWAP_COUNT: int = 1
    # STARKVERSE_NFT_MINT_COUNT: int = 1
    # STARKNETID_NFT_MINT_COUNT: int = 1
    # JEDISWAP_SWAP_PERCENTAGE: int = random.randint(55, 75)
    # JEDISWAP_LIQ_PERCENTAGE: int = random.randint(70, 80)
    # AVNUFI_SWAP_PERCENTAGE: int = random.randint(55, 75)
    # TENK_SWAP_PERCENTAGE: int = random.randint(55, 75)
    # DMAIL_MESSAGES_COUNT: int = 2


class TaskPrep:
    def __init__(self, client, route: int, params):
        self.JediSwap_client = JediSwap(client=client, JEDISWAP_SWAP_PERCENTAGE=params.JEDISWAP_SWAP_PERCENTAGE,
                                   JEDISWAP_LIQ_PERCENTAGE=params.JEDISWAP_LIQ_PERCENTAGE,
                                   SLIPPAGE=params.SWAP_SLIPPAGE)
        self.AvnuFi_client = AvnuFi(client=client, AVNUFI_SWAP_PERCENTAGE=params.AVNUFI_SWAP_PERCENTAGE,
                               SLIPPAGE=params.SWAP_SLIPPAGE)
        self.TenkSwap_client = TenkSwap(client=client, TENK_SWAP_PERCENTAGE=params.TENK_SWAP_PERCENTAGE,
                                   SLIPPAGE=params.SWAP_SLIPPAGE)
        self.Minter_client = Stark_Minter(client=client)
        self.Dmail_client = Dmail(client=client)
        self.route = route

    def get_tasks(self):
        TASKS = []
        if self.route == 0:
                #TASKS.append((f"JediSwap Swap", self.JediSwap_client.swap))

                #TASKS.append((f"AvnuFi Swap", self.AvnuFi_client.swap))

                #TASKS.append((f"10kSwap Swap", self.TenkSwap_client.swap))

                TASKS.append((f"StarkVerseNFT Minting", self.Minter_client.mintStarkVerse))

                #TASKS.append((f"StarkNetIDNFT Minting", self.Minter_client.mintStarknetIdNFT))

                #TASKS.append((f"Dmail message", self.Dmail_client.send_message))

                random.shuffle(TASKS)

                #TASKS.append(("JediSwap Liquidity Adding", JediSwap_client.add_liquidity))

        elif self.route == 1:

            for i in range(2):
                TASKS.append((f"JediSwap Swap {i + 1}", JediSwap_client.swap))

            for i in range(2):
                TASKS.append((f"AvnuFi Swap {i + 1}", AvnuFi_client.swap))

            for i in range(2):
                TASKS.append((f"10kSwap Swap {i + 1}", TenkSwap_client.swap))

            for i in range(2):
                TASKS.append((f"StarkVerseNFT Minting {i + 1}", Minter_client.mintStarkVerse))

            for i in range(2):
                TASKS.append((f"StarkNetIDNFT Minting {i + 1}", Minter_client.mintStarknetIdNFT))

            for i in range(3):
                TASKS.append((f"Dmail message {i + 1}", Dmail_client.send_message))

            random.shuffle(TASKS)

            #TASKS.append(("JediSwap Liquidity Adding", JediSwap_client.add_liquidity))

        elif self.route == 2:

            for i in range(3):
                TASKS.append((f"JediSwap Swap {i + 1}", JediSwap_client.swap))

            for i in range(3):
                TASKS.append((f"AvnuFi Swap {i + 1}", AvnuFi_client.swap))

            for i in range(2):
                TASKS.append((f"10kSwap Swap {i + 1}", TenkSwap_client.swap))

            for i in range(4):
                TASKS.append((f"StarkVerseNFT Minting {i + 1}", Minter_client.mintStarkVerse))

            for i in range(3):
                TASKS.append((f"StarkNetIDNFT Minting {i + 1}", Minter_client.mintStarknetIdNFT))

            for i in range(8):
                TASKS.append((f"Dmail message {i + 1}", Dmail_client.send_message))

            random.shuffle(TASKS)

            TASKS.append(("JediSwap Liquidity Adding", JediSwap_client.add_liquidity))

        return TASKS


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
    reply_message += f"<b>🎡 Starknet script includes: </b>\n\n" \
                     f"<b>Interaction with dexes: </b>\n\n" \
                     "       🔸 <i>JediSwap ( Swaps; Liquidity Adding)</i>\n" \
                     "       🔸 <i>AvnuFi (Swaps)</i>\n" \
                     "       🔸 <i>10K Swap (Swaps)</i>\n" \
                     "       🔸 <i>Dmail (Message sender)</i>\n\n" \
                     f"<b>NFT mint : </b>\n\n" \
                     "       🔸 <i>StarkNetID NFT</i>\n" \
                     "       🔸 <i>StarkVerse NFT</i>\n\n" \

    total_time = "45"
    reply_message += f"🕔 <b>Total time</b> ~ {total_time} mins *\n\n" \
                     f"<i>* We stretch out time to imitate how humans act</i>\n\n"


    await bot.edit_message_text(chat_id=wait_message.chat.id,
                                message_id=wait_message.message_id,
                                text=f"⏳ Preparing information about the script ... 100% ...")

    b1 = KeyboardButton("🐳 LFG!")
    # b2 = KeyboardButton("⛔️ Stop ⛔️")
    b3 = KeyboardButton("⬅ Go to menu")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.row(b1).row(b3)

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
                params = RunningParams()

                client = Client(address=int(private_keys[i+1][0], 16),
                                private_key=int(private_keys[i+1][1], 16),
                                address_to_log=private_keys[i+1][0],
                                starknet_rpc=params.STARKNET_RPC,
                                MAX_GWEI=3000)

                ########################################### DEPLOYING IF NEEDED #################################
                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"⏳ _Deploying wallet if needed..._", parse_mode=types.ParseMode.MARKDOWN)

                deploy_result = await client.deploy()
                if deploy_result:
                    await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                message_id=wait_message.message_id,
                                                text=f"⏳ _Wallet was successfully deployed_",
                                                parse_mode=types.ParseMode.MARKDOWN)
                    await asyncio.sleep(2)

                ########################################### TASKS PREPARING #################################
                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"⏳ _Preparing tasks..._", parse_mode=types.ParseMode.MARKDOWN)

                user_data = await state.get_data()
                if user_data.get("stop_flag"):
                    return

                data = await state.get_data()
                is_test_stark = data.get("is_test_stark")
                is_medium_stark = data.get("is_medium_stark")
                is_hard_stark = data.get("is_hard_stark")

                TASKS=[]

                if is_test_stark == 1:
                    TP = TaskPrep(client=client, params=params, route=0)
                    TASKS = TP.get_tasks()

                elif is_medium_stark == 1:
                    TP = TaskPrep(client=client, params=params, route=1)
                    TASKS = TP.get_tasks()

                elif is_hard_stark == 1:
                    TP = TaskPrep(client=client, params=params, route=2)
                    TASKS = TP.get_tasks()

                wallet_statistics = {task_name: "" for task_name, _ in TASKS}

                ########################################### TASKS PERFORMING #################################

                start_delay = random.randint(30, 60)

                user_data = await state.get_data()
                if user_data.get("stop_flag"):
                    return

                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"⏳ *[{client.address_to_log}]* Sleeping for _{start_delay} s_ "
                                                 f"before starting script",
                                            parse_mode=types.ParseMode.MARKDOWN)

                one_wallet_run_price = get_one_wallet_run_price()
                is_free_run = user_db.is_free_run(message.from_user.id)  # 1 == free

                if is_free_run == 0:
                    user_db.update_balance(message.from_user.id, -(len(private_keys) * one_wallet_run_price))

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

                    delay = random.randint(45, 90)
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

                        # elif "Client failed with code 63" in str(err):
                        #     logger.error(f"[{client.address_to_log}] {err}")
                        #     try:
                        #         retry_delay = random.randint(15, 30)
                        #         logger.info(f"[{client.address_to_log}] Sleeping for {retry_delay} s before retrying")
                        #
                        #         await bot.edit_message_text(chat_id=wait_message.chat.id,
                        #                                     message_id=wait_message.message_id,
                        #                                     text=f"❌ *[{client.address_to_log}]* Sleeping for _{retry_delay} s_ before retrying",
                        #                                     parse_mode=types.ParseMode.MARKDOWN)
                        #
                        #         await asyncio.sleep(retry_delay)
                        #         await task()
                        #         wallet_statistics[task_name] = "✅"
                        #
                        #         current_statistic += f"{task_name}: <i>✅</i>\n"
                        #         await state.update_data(final_statistic_stark=current_statistic)

                            # except Exception as retry_err:
                            #     logger.error(f"[{client.address_to_log}] Error while retrying task after 63 error: {retry_err}")
                            #     await bot.edit_message_text(chat_id=wait_message.chat.id,
                            #                                 message_id=wait_message.message_id,
                            #                                 text=f"❌ *[{client.address_to_log}]* Error while retrying task after 63 error: _{retry_err}_",
                            #                                 parse_mode=types.ParseMode.MARKDOWN)
                            #
                            #     wallet_statistics[task_name] = "❌ Client failed"
                            #
                            #     current_statistic += f"{task_name}: <i>❌ Client failed</i>\n"
                            #     await state.update_data(final_statistic_stark=current_statistic)
                        elif "Insufficient tokens on balance to add a liquidity pair. Only ETH is available" in str(err):
                            logger.error(f"[{client.address_to_log}] {err}")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"❌ *[{client.address_to_log}]* _{err}_",
                                                        parse_mode=types.ParseMode.MARKDOWN)

                            wallet_statistics[task_name] = "❌ Insufficient tokens on balance to add a liquidity pair"

                            current_statistic += f"{task_name}: <i>❌ Insufficient tokens on balance to add a liquidity pair</i>\n"
                            await state.update_data(final_statistic_stark=current_statistic)
                        # elif "host starknet-mainnet.infura.io" in str(err):
                        #     logger.error(f"[{client.address_to_log}] {err}")
                        #     await bot.edit_message_text(chat_id=wait_message.chat.id,
                        #                                 message_id=wait_message.message_id,
                        #                                 text=f"❌ *[{client.address_to_log}]* _{err}_",
                        #                                 parse_mode=types.ParseMode.MARKDOWN)
                        #     try:
                        #         user_data = await state.get_data()
                        #         if user_data.get("stop_flag"):
                        #             return
                        #
                        #         retry_delay = random.randint(15, 30)
                        #
                        #         await bot.edit_message_text(chat_id=wait_message.chat.id,
                        #                                     message_id=wait_message.message_id,
                        #                                     text=f"*[{client.address_to_log}]* Sleeping for _{retry_delay} s_ before retrying",
                        #                                     parse_mode=types.ParseMode.MARKDOWN)
                        #
                        #         await asyncio.sleep(retry_delay)
                        #
                        #         user_data = await state.get_data()
                        #         if user_data.get("stop_flag"):
                        #             return
                        #
                        #         TOTAL_SLEEP_TIME += retry_delay
                        #         await task()
                        #         wallet_statistics[task_name] = "✅"
                        #         current_statistic += f"{task_name}: <i>✅</i>\n"
                        #     except Exception as retry_err:
                        #         logger.error(
                        #             f"[{client.address_to_log}] Error while retrying task after connection issue: {retry_err}")
                        #         await bot.edit_message_text(chat_id=wait_message.chat.id,
                        #                                     message_id=wait_message.message_id,
                        #                                     text=f"*[{client.address_to_log}]* Error while retrying task after connection issue: _{retry_err}_",
                        #                                    parse_mode=types.ParseMode.MARKDOWN)
                        #         wallet_statistics[task_name] = "❌ Lost connection with starknet-mainnet.infura.io"
                        #
                        #         current_statistic += f"{task_name}: <i>❌ Lost connection with starknet-mainnet.infura.io</i>\n"
                        #         await state.update_data(final_statistic_stark=current_statistic)

                        elif "Transaction reverted: Error in the called contract." in str(err):
                            logger.error(f"[{client.address_to_log}] {err}")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"*[{client.address_to_log}]* _Transaction reverted: Error in the called contract_",
                                                        parse_mode=types.ParseMode.MARKDOWN)

                            wallet_statistics[task_name] = "❌ Transaction reverted: Error in the called contract"

                            current_statistic += f"{task_name}: <i>❌ Transaction reverted: Error in the called contract</i>\n"
                            await state.update_data(final_statistic_stark=current_statistic)

                        elif "object has no attribute" in str(err):
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
                                logger.error(f"[{client.address_to_log}] Error while retrying task after error: {retry_err}")
                                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                            message_id=wait_message.message_id,
                                                            text=f"❌ *[{client.address_to_log}]* Error while retrying task after error: _{retry_err}_",
                                                            parse_mode=types.ParseMode.MARKDOWN)

                                wallet_statistics[task_name] = "❌ Client failed (NoneType Val)"

                                current_statistic += f"{task_name}: <i>❌ Client failed (NoneType Val)</i>\n"
                                await state.update_data(final_statistic_stark=current_statistic)
            
                        else:
                            logger.error(f"[{client.address_to_log}] Error while performing task: {err}")
                            err_escaped = str(err)
                            if "max_fee" in str(err):
                                error = str(err)
                                err_escaped = error.replace("max_fee", "maxfee")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"*[{client.address_to_log}]* Error while performing task: _{err_escaped}_",
                                                        parse_mode=types.ParseMode.MARKDOWN)

                            wallet_statistics[task_name] = f"❌ {err_escaped}"

                            current_statistic += f"{task_name}: <i>❌ {err_escaped}</i>\n"
                            await state.update_data(final_statistic_stark=current_statistic)

                import re
                def sort_key(item):
                    match = re.match(r"([a-zA-Z\s]+)(\d*)", item[0])
                    if match:
                        name, number = match.groups()
                        return name, int(number) if number else 0
                    else:
                        # Возвращаем какое-то дефолтное значение или обрабатываем исключение
                        return item[0], 0
                print(wallet_statistics)
                sorted_statistics = sorted(wallet_statistics.items(), key=sort_key)
                print(sorted_statistics)
                # формирование финального сообщения
                final_statistic += f"\nWallet <b>[{client.address_to_log}]</b>\n\n"

                for task_name, status in sorted_statistics:
                    final_statistic += f"{task_name}: <i>{status}</i>\n"

            except Exception as err:
                logger.error(f"#{i} Something went wrong while client declaring or getting params: {err}")
                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"#{i} Something went wrong while client declaring or getting params: _{err}_",
                                            parse_mode=types.ParseMode.MARKDOWN)

        is_free_run = user_db.is_free_run(message.from_user.id)  # 1 == free

        await state.update_data(is_ready=0)
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
            congratulations = "\n\n🎉 Congratulations, Arnold AIO has successfully done <b>Starknet script</b> for you! \n\n" \
                              "😤 In the past, the average web3 user has made $550 per wallet for doing the same actions in airdrops. \n\n" \
                              "⬇️If you want to run another wallet - top up your balance in the <b>💵 Balance and deposit</b> section!"

            await message.answer(congratulations,
                                 parse_mode=types.ParseMode.HTML,
                                 reply_markup=reply_markup)

    else:
            b1 = KeyboardButton("🐳 LFG!")
            # b2 = KeyboardButton("⛔️ Stop ⛔️")
            b3 = KeyboardButton("⬅ Go to menu")

            buttons = ReplyKeyboardMarkup(resize_keyboard=True)
            buttons.row(b1).row(b3)

            is_ready = 0
            await state.update_data(is_ready=is_ready)
            await message.answer(f"❗️ *Wait for wallet processing*", parse_mode=types.ParseMode.MARKDOWN,
                                 reply_markup=buttons)
