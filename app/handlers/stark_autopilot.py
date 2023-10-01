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

one_wallet_run_price = 5


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
    #
    # average_time_of_bridge = Randomiser.average_time(len_pk, Randomiser.random_bridge)
    # average_time_after_bridge = Randomiser.average_time(len_pk, Randomiser.random_bridge_after)
    # average_time_of_create = Randomiser.average_time(len_pk, Randomiser.random_contract)
    # average_time_after_create = Randomiser.average_time(len_pk, Randomiser.random_contract_after)
    # average_time_of_warm_up = 3 * Randomiser.average_time(len_pk, Randomiser.random_warm_up)
    # average_time_after_warm_up = 3 * Randomiser.average_time(len_pk, Randomiser.random_warm_up_after)
    # average_time_of_mint_erc_721 = 7 * Randomiser.average_time(len_pk, Randomiser.random_mint)
    # average_time_of_mint_erc_1155 = 2 * Randomiser.average_time(len_pk, Randomiser.random_mint)
    # average_time_after_mints = 8 * Randomiser.average_time(len_pk, Randomiser.random_mint_after)
    # total_time = int(
    #     (average_time_of_bridge + average_time_after_bridge + average_time_of_create + average_time_after_create
    #      + average_time_after_warm_up + average_time_after_warm_up + average_time_of_mint_erc_721
    #      + average_time_of_mint_erc_1155 + average_time_after_mints) / 60)
    #
    # await bot.edit_message_text(chaet_id=wait_message.chat.id,
    #                             message_id=wait_message.message_id,
    #                             text=f"⏳ Preparing information about the script ... 50% ...")
    #
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
    b3 = KeyboardButton("⬅ Go to menu")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.row(b1, b2).row(b3)

    is_ready = 0
    await state.update_data(is_ready=is_ready)
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

    if "final_statistic" in data:
        message_response += data.get("final_statistic")

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
async def start_earn(message: types.Message, state: FSMContext):
    data = await state.get_data()
    is_ready = data.get("is_ready")
    TOTAL_SLEEP_TIME = 0

    if is_ready == 0:

        is_ready = -1
        await state.update_data(is_ready=is_ready)
        private_keys = dict(data.get("private_keys"))

        count_keys = len(private_keys)

        final_statistic = "\n📊📊📊📊📊📊📊 <b>Statistic</b> \n\n"

        wait_message = await message.answer("Taking off ✈️...")

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
                                            text=f"⏳ Preparing tasks...")

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
                logger.info(f"[{client.address_to_log}] Sleeping for {start_delay} s before taking off")

                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"⏳[{client.address_to_log}] Sleeping for {start_delay} s before taking off")

                await asyncio.sleep(start_delay)
                TOTAL_SLEEP_TIME += start_delay

                final_statistic += f"\n <u> <b> {client.address_to_log} </b> </u> \n"

                log_counter = 0
                for task_name, task in TASKS:
                    params = RunningParams()  # новый объект для генерации нового рандом делея
                    delay = params.RANDOM_DELAY
                    if log_counter != 0:
                        logger.info(f"[{client.address_to_log}] Sleeping for {delay} s before doing next task")

                        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                    message_id=wait_message.message_id,
                                                    text=f"[{client.address_to_log}] Sleeping for {delay} s before doing next task")
                        await asyncio.sleep(delay)
                        TOTAL_SLEEP_TIME += delay
                    try:
                        balance = (await client.get_balance()).Ether
                        if balance >= 0.000055:
                            await task()
                            wallet_statistics[task_name] = "✅"
                            log_counter = 1
                        else:
                            logger.error(
                                f"[{client.address_to_log}] Insufficient funds in StarkNet. Balance: {balance} ETH")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"[{client.address_to_log}] Insufficient funds. Balance: {balance} ETH")

                            # заполнение оставшейся статистики крестиками в случае нехватки денег
                            for remaining_task_name, _ in TASKS[TASKS.index((task_name, task)):]:
                                wallet_statistics[remaining_task_name] = f"❌ Insufficient funds. Balance: {balance} ETH"
                            break
                    except Exception as err:
                        if "nonce" in str(err):
                            logger.error(f"[{client.address_to_log}] Invalid transaction nonce")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"[{client.address_to_log}] Invalid transaction nonce")
                            wallet_statistics[task_name] = "❌ Invalid transaction nonce"
                        elif "Insufficient tokens on balance to add a liquidity pair. Only ETH is available" in str(
                                err):
                            logger.error(f"[{client.address_to_log}] {err}")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"[{client.address_to_log}] {err}")
                            wallet_statistics[task_name] = "❌ Insufficient tokens on balance to add a liquidity pair"
                        elif "host starknet-mainnet.infura.io" in str(err):
                            logger.error(f"[{client.address_to_log}] {err}")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"[{client.address_to_log}] {err}")
                            try:
                                retry_delay = random.randint(15, 30)
                                logger.info(f"[{client.address_to_log}] Sleeping for {retry_delay} s before retrying")
                                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                            message_id=wait_message.message_id,
                                                            text=f"[{client.address_to_log}] Sleeping for {retry_delay} s before retrying")
                                await asyncio.sleep(retry_delay)
                                TOTAL_SLEEP_TIME += retry_delay
                                await task()
                                wallet_statistics[task_name] = "✅"
                            except Exception as retry_err:
                                logger.error(
                                    f"[{client.address_to_log}] Error while retrying task after connection issue: {retry_err}")
                                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                            message_id=wait_message.message_id,
                                                            text=f"[{client.address_to_log}] Error while retrying task after connection issue: {retry_err}")
                                wallet_statistics[task_name] = "❌ Lost connection with starknet-mainnet.infura.io"

                        elif "Transaction reverted: Error in the called contract." in str(err):
                            logger.error(f"[{client.address_to_log}] {err}")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"[{client.address_to_log}] Transaction reverted: Error in the called contract")
                            wallet_statistics[task_name] = "❌ Transaction reverted: Error in the called contract"

                        else:
                            logger.error(f"[{client.address_to_log}] Error while performing task: {err}")
                            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                        message_id=wait_message.message_id,
                                                        text=f"[{client.address_to_log}] Error while performing task: {err}")
                            wallet_statistics[task_name] = f"❌ Error while performing task: {err}"

                    # формирую финальное сообщение о статистике исходя из собранной статистики одного прогнанного кошелька
                    final_statistic += f"\n<u><b>{client.address_to_log}</b></u>\n"

                    for task_name, status in wallet_statistics.items():
                        final_statistic += f"<u>{task_name} </u>: {status}\n"

            except Exception as err:
                logger.error(f"#{i} Something went wrong while client declaring or getting params: {err}")
                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"#{i} Something went wrong while client declaring or getting params: {err}")

        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"Preparing statistics...")

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
#
#         await state.update_data(final_statistic=final_statistic)
#
#         #############################################################################################
#
#         sleep_on_0 = Randomiser.random_bridge_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=bridge_statistic + f"\n Sleeping on {sleep_on_0} sec ...")
#         await asyncio.sleep(sleep_on_0)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         ########################################## CONTRACT  ###########################################
#
#         random_names = list(animals.animals.keys())
#         random_symbols = list(animals.animals.values())
#         random_desc = list(desc_list.description)
#
#         random.shuffle(random_names)
#         random.shuffle(random_symbols)
#         random.shuffle(random_desc)
#
#         random_names = random_names[:count_private_keys]
#         random_symbols = random_symbols[:count_private_keys]
#         random_desc = random_desc[:count_private_keys]
#
#         mintPrice_list = [Randomiser.mintPrice() for _ in range(count_private_keys)]
#         mintLimitPerAddress_list = [Randomiser.mintLimitPerAddress() for _ in range(count_private_keys)]
#         editionSize_list = [Randomiser.editionSize() for _ in range(count_private_keys)]
#         royaltyBPS_list = [Randomiser.royaltyBPS() for _ in range(count_private_keys)]
#         imageURI_list = []
#
#         for elem in imageURI_list_hashes:
#             imageURI_list.append("ipfs://" + elem)
#         random.shuffle(imageURI_list)
#
#         contract_counter = 1
#         list_of_contract_result = []
#         final_statistic += "\n <u> NFT create </u> \n"
#         wait_message_text = "📊 Statistic \n\n" \
#                             " NFT create \n"
#
#         for minter, name, symbol, description, mintPrice, \
#             mintLimitPerAddress, editionSize, royaltyBPS, imageURI in zip(minters_obj, random_names, random_symbols,
#                                                                           random_desc,
#                                                                           mintPrice_list, mintLimitPerAddress_list,
#                                                                           editionSize_list, royaltyBPS_list,
#                                                                           imageURI_list):
#             result = await minter.createERC721(name=name, symbol=symbol, description=description, mintPrice=mintPrice,
#                                                mintLimitPerAddress=mintLimitPerAddress,
#                                                editionSize=editionSize, royaltyBPS=royaltyBPS, imageURI=imageURI)
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             list_of_contract_result.append(result)
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Creating ERC721 {contract_counter}/{count_private_keys}")
#             contract_counter += 1
#
#             await asyncio.sleep(Randomiser.random_contract())
#
#         for i in range(len(list_of_contract_result)):
#             final_statistic += f"Wallet {i + 1}: {list_of_contract_result[i]} \n"
#             wait_message_text += f"Wallet {i + 1}: {list_of_contract_result[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         #############################################################################################
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         sleep_on_1 = Randomiser.random_contract_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=wait_message_text + f"\nSleeping on {sleep_on_1} sec ...")
#         await asyncio.sleep(sleep_on_1)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         ########################################## WARM UP  ###########################################
#
#         warm_up_statistic = "📊 Statistic \n\n" \
#                             " Warm Up #1 \n"
#
#         final_statistic += "\n <u> Warm Up #1 </u> \n"
#
#         # 1
#         warm_up_counter_1 = 1
#         warm_up_result_1_list = []
#         for minter in minters_obj:
#             result1 = await minter.walletWarmUp1(minter.collectionAddress, Minter.generateUri())
#             warm_up_result_1_list.append(result1)
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Warm up #1  {warm_up_counter_1}/{count_private_keys}")
#             warm_up_counter_1 += 1
#
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_warm_up())
#
#         for i in range(len(warm_up_result_1_list)):
#             final_statistic += f"Wallet {i + 1}: {warm_up_result_1_list[i]} \n"
#             warm_up_statistic += f"Wallet {i + 1}: {warm_up_result_1_list[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         sleep_on_warm_up_1 = Randomiser.random_warm_up_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=warm_up_statistic + f"\nSleeping on {sleep_on_warm_up_1} sec ...")
#         await asyncio.sleep(sleep_on_warm_up_1)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         # 2
#         warm_up_statistic += "\n Warm Up #2 \n"
#         final_statistic += "\n <u> Warm Up #2 </u> \n"
#
#         warm_up_counter_2 = 1
#         warm_up_result_2_list = []
#         for minter in minters_obj:
#             result2 = await minter.walletWarmUp2(minter.collectionAddress, round(random.uniform(0.00001, 150), 5))
#             warm_up_result_2_list.append(result2)
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Warm up #2  {warm_up_counter_2}/{count_private_keys}")
#             warm_up_counter_2 += 1
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_warm_up())
#
#         for i in range(len(warm_up_result_2_list)):
#             final_statistic += f"Wallet {i + 1}: {warm_up_result_2_list[i]} \n"
#             warm_up_statistic += f"Wallet {i + 1}: {warm_up_result_2_list[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         sleep_on_warm_up_2 = Randomiser.random_warm_up_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=warm_up_statistic + f"\nSleeping on {sleep_on_warm_up_2} sec ...")
#         await asyncio.sleep(sleep_on_warm_up_2)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         # 3
#         warm_up_statistic += "\n Warm Up #3 \n"
#         final_statistic += "\n <u> Warm Up #3 </u> \n"
#
#         warm_up_counter_3 = 1
#         warm_up_result_3_list = []
#         for minter in minters_obj:
#             result3 = await minter.walletWarmUp2(minter.collectionAddress, round(random.uniform(0.00001, 150), 5))
#             warm_up_result_3_list.append(result3)
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Warm up #3  {warm_up_counter_3}/{count_private_keys}")
#             warm_up_counter_3 += 1
#
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_warm_up())
#
#         for i in range(len(warm_up_result_3_list)):
#             final_statistic += f"Wallet {i + 1}: {warm_up_result_3_list[i]} \n"
#             warm_up_statistic += f"Wallet {i + 1}: {warm_up_result_3_list[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         #############################################################################################
#
#         sleep_on_warm_up_3 = Randomiser.random_warm_up_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=warm_up_statistic + f"\nSleeping on {sleep_on_warm_up_3} sec ...")
#         await asyncio.sleep(sleep_on_warm_up_3)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         ########################################### MINTS  ###########################################
#
#         mints_func = [mint_1, mint_2, mint_3, mint_4, mint_5, mint_6, mint_7, mint_8, mint_9]
#         minters_obj_for_mint = [Minter(private_key) for private_key in private_keys]
#         used_functions_by_minters = {minter: [] for minter in minters_obj_for_mint}
#
#         # 1
#         mint_statistic = "📊 Statistic \n\n" \
#                          " Mint #1 \n"
#
#         final_statistic += "\n <u> Mint #1 </u> \n"
#
#         mint_1_counter = 1
#         mint_1_result_list = []
#
#         random.shuffle(mints_func)
#
#         for minter in minters_obj_for_mint:
#             while mints_func[0] in used_functions_by_minters[minter]:
#                 random.shuffle(mints_func)
#
#             used_functions_by_minters[minter].append(mints_func[0])
#
#             mint_1_result = await mints_func[0](minter)
#
#             if mint_1_result is None:
#                 mint_1_result = "❌ Something went wrong"
#
#             mint_1_result_list.append(mint_1_result)
#             random.shuffle(mints_func)
#
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Mint #1  {mint_1_counter}/{count_private_keys}")
#             mint_1_counter += 1
#
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_mint())
#
#         for i in range(len(mint_1_result_list)):
#             final_statistic += f"Wallet {i + 1}: {mint_1_result_list[i]} \n"
#             mint_statistic += f"Wallet {i + 1}: {mint_1_result_list[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         sleep_on = Randomiser.random_mint_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
#         await asyncio.sleep(sleep_on)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         # 2
#         mint_statistic += "\n Mint #2 \n"
#         final_statistic += "\n <u> Mint #2 </u> \n"
#
#         mint_2_counter = 1
#         mint_2_result_list = []
#         for minter in minters_obj_for_mint:
#             while mints_func[1] in used_functions_by_minters[minter]:
#                 random.shuffle(mints_func)
#             used_functions_by_minters[minter].append(mints_func[1])
#
#             mint_2_result = await mints_func[1](minter)
#
#             if mint_2_result is None:
#                 mint_2_result = "❌ Something went wrong"
#
#             mint_2_result_list.append(mint_2_result)
#             random.shuffle(mints_func)
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Mint #2  {mint_2_counter}/{count_private_keys}")
#             mint_2_counter += 1
#
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_mint())
#
#         for i in range(len(mint_2_result_list)):
#             final_statistic += f"Wallet {i + 1}: {mint_2_result_list[i]} \n"
#             mint_statistic += f"Wallet {i + 1}: {mint_2_result_list[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         sleep_on = Randomiser.random_mint_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
#         await asyncio.sleep(sleep_on)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         # 3
#         mint_statistic += "\n Mint #3 \n"
#         final_statistic += "\n <u> Mint #3 </u> \n"
#
#         mint_3_counter = 1
#         mint_3_result_list = []
#         for minter in minters_obj_for_mint:
#             while mints_func[2] in used_functions_by_minters[minter]:
#                 random.shuffle(mints_func)
#             used_functions_by_minters[minter].append(mints_func[2])
#
#             mint_3_result = await mints_func[2](minter)
#
#             if mint_3_result is None:
#                 mint_3_result = "❌ Something went wrong"
#             mint_3_result_list.append(mint_3_result)
#             random.shuffle(mints_func)
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Mint #3  {mint_3_counter}/{count_private_keys}")
#             mint_3_counter += 1
#
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_mint())
#
#         for i in range(len(mint_3_result_list)):
#             final_statistic += f"Wallet {i + 1}: {mint_3_result_list[i]} \n"
#             mint_statistic += f"Wallet {i + 1}: {mint_3_result_list[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         sleep_on = Randomiser.random_mint_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
#         await asyncio.sleep(sleep_on)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         # 4
#         mint_statistic += "\n Mint #4 \n"
#         final_statistic += "\n <u> Mint #4 </u> \n"
#
#         mint_4_counter = 1
#         mint_4_result_list = []
#
#         for minter in minters_obj_for_mint:
#             while mints_func[3] in used_functions_by_minters[minter]:
#                 random.shuffle(mints_func)
#             used_functions_by_minters[minter].append(mints_func[3])
#
#             mint_4_result = await mints_func[3](minter)
#
#             if mint_4_result is None:
#                 mint_4_result = "❌ Something went wrong"
#
#             mint_4_result_list.append(mint_4_result)
#             random.shuffle(mints_func)
#
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Mint #4  {mint_4_counter}/{count_private_keys}")
#             mint_4_counter += 1
#
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_mint())
#
#         for i in range(len(mint_4_result_list)):
#             final_statistic += f"Wallet {i + 1}: {mint_4_result_list[i]} \n"
#             mint_statistic += f"Wallet {i + 1}: {mint_4_result_list[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         sleep_on = Randomiser.random_mint_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
#         await asyncio.sleep(sleep_on)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         # 5
#         mint_statistic += "\n Mint #5 \n"
#         final_statistic += "\n <u> Mint #5 </u> \n"
#
#         mint_5_counter = 1
#         mint_5_result_list = []
#
#         for minter in minters_obj_for_mint:
#             while mints_func[4] in used_functions_by_minters[minter]:
#                 random.shuffle(mints_func)
#             used_functions_by_minters[minter].append(mints_func[4])
#
#             mint_5_result = await mints_func[4](minter)
#
#             if mint_5_result is None:
#                 mint_5_result = "❌ Something went wrong"
#
#             mint_5_result_list.append(mint_5_result)
#             random.shuffle(mints_func)
#
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Mint #5  {mint_5_counter}/{count_private_keys}")
#             mint_5_counter += 1
#
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_mint())
#
#         for i in range(len(mint_5_result_list)):
#             final_statistic += f"Wallet {i + 1}: {mint_5_result_list[i]} \n"
#             mint_statistic += f"Wallet {i + 1}: {mint_5_result_list[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         sleep_on = Randomiser.random_mint_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
#         await asyncio.sleep(sleep_on)
#         user_data = await state.get_data()
#
#         if user_data.get("stop_flag"):
#             return
#
#         # 6
#         mint_statistic += "\n Mint #6 \n"
#         final_statistic += "\n <u> Mint #6 </u> \n"
#
#         mint_6_counter = 1
#         mint_6_result_list = []
#
#         for minter in minters_obj_for_mint:
#             while mints_func[5] in used_functions_by_minters[minter]:
#                 random.shuffle(mints_func)
#             used_functions_by_minters[minter].append(mints_func[5])
#
#             mint_6_result = await mints_func[5](minter)
#
#             if mint_6_result is None:
#                 mint_6_result = "❌ Something went wrong"
#
#             mint_6_result_list.append(mint_6_result)
#             random.shuffle(mints_func)
#
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Mint #6  {mint_6_counter}/{count_private_keys}")
#             mint_6_counter += 1
#
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_mint())
#
#         for i in range(len(mint_6_result_list)):
#             final_statistic += f"Wallet {i + 1}: {mint_6_result_list[i]} \n"
#             mint_statistic += f"Wallet {i + 1}: {mint_6_result_list[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         sleep_on = Randomiser.random_mint_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
#         await asyncio.sleep(sleep_on)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         # 7
#         mint_statistic += "\n Mint #7 \n"
#         final_statistic += "\n <u> Mint #7 </u> \n"
#
#         mint_7_counter = 1
#         mint_7_result_list = []
#
#         for minter in minters_obj_for_mint:
#             while mints_func[6] in used_functions_by_minters[minter]:
#                 random.shuffle(mints_func)
#             used_functions_by_minters[minter].append(mints_func[6])
#
#             mint_7_result = await mints_func[6](minter)
#
#             if mint_7_result is None:
#                 mint_7_result = "❌ Something went wrong"
#
#             mint_7_result_list.append(mint_7_result)
#             random.shuffle(mints_func)
#
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Mint #7  {mint_7_counter}/{count_private_keys}")
#             mint_7_counter += 1
#
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_mint())
#
#         for i in range(len(mint_7_result_list)):
#             final_statistic += f"Wallet {i + 1}: {mint_7_result_list[i]} \n"
#             mint_statistic += f"Wallet {i + 1}: {mint_7_result_list[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         sleep_on = Randomiser.random_mint_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
#         await asyncio.sleep(sleep_on)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         # 8
#         mint_statistic += "\n Mint #8 \n"
#         final_statistic += "\n <u> Mint #8 </u> \n"
#
#         mint_8_counter = 1
#         mint_8_result_list = []
#         for minter in minters_obj_for_mint:
#             while mints_func[7] in used_functions_by_minters[minter]:
#                 random.shuffle(mints_func)
#             used_functions_by_minters[minter].append(mints_func[7])
#
#             mint_8_result = await mints_func[7](minter)
#
#             if mint_8_result is None:
#                 mint_8_result = "❌ Something went wrong"
#
#             mint_8_result_list.append(mint_8_result)
#             random.shuffle(mints_func)
#
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Mint #8  {mint_8_counter}/{count_private_keys}")
#             mint_8_counter += 1
#
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_mint())
#
#         for i in range(len(mint_8_result_list)):
#             final_statistic += f"Wallet {i + 1}: {mint_8_result_list[i]} \n"
#             mint_statistic += f"Wallet {i + 1}: {mint_8_result_list[i]} \n"
#
#         await state.update_data(final_statistic=final_statistic)
#
#         sleep_on = Randomiser.random_mint_after()
#         await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                     message_id=wait_message.message_id,
#                                     text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
#         await asyncio.sleep(sleep_on)
#
#         user_data = await state.get_data()
#         if user_data.get("stop_flag"):
#             return
#
#         # 9
#         mint_statistic += "\n Mint #9 \n"
#         final_statistic += "\n <u> Mint #9 </u> \n"
#
#         mint_9_counter = 1
#         mint_9_result_list = []
#
#         for minter in minters_obj_for_mint:
#             while mints_func[8] in used_functions_by_minters[minter]:
#                 random.shuffle(mints_func)
#             used_functions_by_minters[minter].append(mints_func[8])
#
#             mint_9_result = await mints_func[8](minter)
#
#             logger.info(f"🔉 List used_functions_by_minters: {used_functions_by_minters[minter]}")
#
#             if mint_9_result is None:
#                 mint_9_result = "❌ Something went wrong"
#
#             mint_9_result_list.append(mint_9_result)
#             random.shuffle(mints_func)
#
#             await bot.edit_message_text(chat_id=wait_message.chat.id,
#                                         message_id=wait_message.message_id,
#                                         text=f"⏳ Mint #9  {mint_9_counter}/{count_private_keys}")
#             mint_9_counter += 1
#
#             user_data = await state.get_data()
#             if user_data.get("stop_flag"):
#                 return
#
#             await asyncio.sleep(Randomiser.random_mint())
#
#         for i in range(len(mint_9_result_list)):
#             final_statistic += f"Wallet {i + 1}: {mint_9_result_list[i]} \n"
#             mint_statistic += f"Wallet {i + 1}: {mint_9_result_list[i]} \n"
#
#         is_ready_to_start = 0
#         await state.update_data(final_statistic=final_statistic)
#         await state.update_data(is_ready_to_start=is_ready_to_start)
#
#         await bot.delete_message(chat_id=wait_message.chat.id,
#                                  message_id=wait_message.message_id)
#
#         buttons = [
#             KeyboardButton(text="⬅ Go to menu"),
#         ]
#         reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
#                                            resize_keyboard=True)
#         is_ready = 0
#
#         is_free_run = user_db.is_free_run(message.from_user.id)  # 1 == free
#         if is_free_run == 1:
#             user_db.set_false_free_run(message.from_user.id)
#
#         data = await state.get_data()
#         private_keys = list(data.get("private_keys"))
#
#         user_db.update_balance(message.from_user.id, -(len(private_keys) * one_wallet_run_price))
#
#         await state.update_data(is_ready=is_ready)
#         await UserFollowing.wallet_menu.set()
#         await message.answer(final_statistic,
#                              parse_mode=types.ParseMode.HTML,
#                              reply_markup=reply_markup)
#     else:
#         b1 = KeyboardButton("🐳 LFG!")
#         b2 = KeyboardButton("⛔️ Stop ⛔️")
#         b3 = KeyboardButton("⬅ Go to menu")
#
#         buttons = ReplyKeyboardMarkup(resize_keyboard=True)
#         buttons.row(b1, b2).row(b3)
#
#         is_ready = 0
#         await state.update_data(is_ready=is_ready)
#         await message.answer(f"❗️ *Wait for wallet processing*", parse_mode=types.ParseMode.MARKDOWN,
#                              reply_markup=buttons)
