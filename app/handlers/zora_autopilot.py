import asyncio
import random

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.utils.Minter import Minter
from app.utils.Bridger import Bridger
from app.utils.configs import animals
from app.utils.configs import description as desc_list
from app.utils.Randomiser import Randomiser
from app.utils.configs.ipfs import imageURI_list_hashes
from app.utils.Estimate import Estimate
from app.logs import logging as logger


@dp.message_handler(Text(equals="💸 Start script"), state=UserFollowing.choose_point)
async def tap_to_earn(message: types.Message, state: FSMContext):
    reply_message = ""
    count_ok_wallet = 0
    count_bridged_wallets = 0

    data = await state.get_data()

    private_keys = list(data.get("private_keys"))
    bridge_amount = list(data.get("random_amount"))
    is_ready_to_start = data.get("is_ready_to_start")

    if len(private_keys) == 1:
        edit_message = "Waiting for refilling of the wallet...."
    else:
        edit_message = "Waiting for refilling of the wallets...."

    wait_message = await message.answer(edit_message)

    for i, random in zip(range(len(private_keys)), bridge_amount):

        es = Estimate(private_keys[i])
        eth_balance = es.get_eth_balance()

        reply_message += f"{i + 1}. <b>{es.get_eth_address()}</b> "

        await asyncio.sleep(1)
        is_used_bridge = await Bridger.used_bridge(private_keys[i])
        if is_used_bridge:
            reply_message += f"<b>[BRIDGED]</b> (Balance in Zora: {eth_balance} ETH) ✅\n"
            count_ok_wallet += 1
            count_bridged_wallets += 1
        else:
            eth_required = es.eth_required(random)
            reply_message += f"\n({eth_balance} ETH / {eth_required} ETH required)"

            if eth_balance != "-":
                if eth_balance >= eth_required:
                    reply_message += " ✅\n"
                    count_ok_wallet += 1
                else:
                    reply_message += " ❌\n"

            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Waiting for refilling of the wallets ... {i + 1}/{len(private_keys)}")

    if count_ok_wallet == len(private_keys) or is_ready_to_start == 1:

        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Preparing information about the script ... 0% ...")
        len_pk = len(private_keys)

        average_time_of_bridge = Randomiser.average_time((len_pk - count_bridged_wallets), Randomiser.random_bridge)
        average_time_after_bridge = Randomiser.average_time((len_pk - count_bridged_wallets), Randomiser.random_bridge_after)
        average_time_of_create = Randomiser.average_time(len_pk, Randomiser.random_contract)
        average_time_after_create = Randomiser.average_time(len_pk, Randomiser.random_contract_after)
        average_time_of_warm_up = 3 * Randomiser.average_time(len_pk, Randomiser.random_warm_up)
        average_time_after_warm_up = 3 * Randomiser.average_time(len_pk, Randomiser.random_warm_up_after)
        average_time_of_mint_erc_721 = 7 * Randomiser.average_time(len_pk, Randomiser.random_mint)
        average_time_of_mint_erc_1155 = 2 * Randomiser.average_time(len_pk, Randomiser.random_mint)
        average_time_after_mints = 8 * Randomiser.average_time(len_pk, Randomiser.random_mint_after)
        total_time = int(
            (average_time_of_bridge + average_time_after_bridge + average_time_of_create + average_time_after_create
             + average_time_after_warm_up + average_time_after_warm_up + average_time_of_mint_erc_721
             + average_time_of_mint_erc_1155 + average_time_after_mints) / 60)

        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Preparing information about the script ... 50% ...")

        reply_message += f"\n📍 Total сount of wallets: <b>{len_pk}</b>\n\n"
        reply_message += f"<b>Bot superpower's:</b>\n\n"

        if count_ok_wallet == count_bridged_wallets:
            pass
        else:
            reply_message += f"📩 <b>Use official Zora Bridge (Ethereum mainnet —> Zora mainnet)</b> ~ {average_time_of_bridge} mins\n" \
                             f"       Sleep after Bridge ~ {average_time_after_bridge} mins\n\n"

        reply_message += f"🀄️ <b>NFT Creation</b> ~ {average_time_of_create} mins\n" \
                         f"       Sleep after creating ~ {average_time_after_create} mins\n\n"
        reply_message += f"🏋️‍♂ <b>Wallet warm-up's</b> ~ {average_time_of_warm_up} mins\n" \
                         f"       Sleep after all warm-up's ~ {average_time_after_warm_up} mins\n\n"
        reply_message += f"🔀 <b>Randomize mint ERC 1155 NFT'S (2)</b> ~ {average_time_of_mint_erc_1155} mins\n" \
                         "       • <i><a href='https://zora.co/collect/zora:0x4c0c2dd31d2661e8bcec60a42e803dcc6f81baad'>Pattern Recognition</a></i>\n\n" \

        reply_message += f"🔀 <b>Randomize mint ERC 721 NFT'S (7)</b> ~ {average_time_of_mint_erc_721} mins\n" \
                         "       • <i><a href='https://zora.co/collect/zora:0x3f1201a68b513049f0f6e182f742a0dce970d8cd'>Zora Merch - Limited Edition Hoodie</a></i>\n" \
                         "       • <i><a href='https://zora.co/collect/zora:0x34573d139A15e5d3D129AD6AE20c3C8B221fD921'>50M LayerZero Messages</a></i>\n" \
                         "       • <i><a href='https://zora.co/collect/zora:0x4ad3cd57a68149a5c5d8a41919dc8ac02d00a366'>Guild on Zora</a></i>\n" \
                         "       • <i><a href='https://zora.co/collect/zora:0x02a1c9babc92d600818ea11ba5b9547f7f25887c'>LayerZero x Nomis</a></i>\n" \
                         "       • <i><a href='https://zora.co/collect/zora:0xbc8ae1adbfb0052babae00d3211f0be30f1fbd5c'>3NUM Shield Opepen</a></i>\n" \
                         "       • <i><a href='https://zora.co/collect/zora:0xcba60a105b5c2fdaf9dd27e733132cc4f7ac9a66'>Holograph VIP</a></i>\n" \
                         "       • <i><a href='https://zora.co/collect/zora:0xcdc9c8060c7c357ee25cd80455cbe05b226d291f'>WEB3PLOTMANS</a></i>\n" \
                         "       • <i><a href='https://zora.co/collect/zora:0x706bafabdd00ceac5b66600901a2b1d1f4992b9d'>Polyhedra live on Mantle Network Mainnet</a></i>\n" \
                         f"  Sleep after all mints ~ {average_time_after_mints} mins\n\n"

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
        await UserFollowing.tap_to_earn.set()
    else:
        reply_message += "\n 💳 Refill your wallet balance and try again \n\n" \
                         f"\nPlease, deposit ETH amount on your wallet in <b>Ethereum Mainnet Chain</b> \n\n" \
                         f"* <i>Withdrawal takes ~ 5 minutes</i>\n\n " \
                         "<b>⚠️ Be sure to use CEX or you'll link your wallets and become sybil</b>"

        b3 = KeyboardButton("⬅ Go to menu")

        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.row(b3)

    await bot.delete_message(chat_id=wait_message.chat.id,
                             message_id=wait_message.message_id)
    await message.answer(reply_message, parse_mode=types.ParseMode.HTML,
                         reply_markup=buttons)


@dp.message_handler(Text(equals="⛔️ Stop ⛔️"), state=UserFollowing.tap_to_earn)
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


async def mint_1(minter):
    return await minter.purchase("0x3f1201a68b513049f0f6e182f742a0dce970d8cd", value_to_send=0.001554)


async def mint_2(minter):
    return await minter.purchase("0x4ad3cd57a68149a5c5d8a41919dc8ac02d00a366", value_to_send=0.000777)


async def mint_3(minter):
    return await minter.mint("0x4c0c2dd31d2661e8bcec60a42e803dcc6f81baad", 7)


async def mint_4(minter):
    return await minter.purchase("0x34573d139A15e5d3D129AD6AE20c3C8B221fD921", value_to_send=0.001007)


async def mint_5(minter):
    return await minter.purchase("0xbc8ae1adbfb0052babae00d3211f0be30f1fbd5c", value_to_send=0.000777)


async def mint_6(minter):
    return await minter.purchase("0xcba60a105b5c2fdaf9dd27e733132cc4f7ac9a66", value_to_send=0.000777)


async def mint_7(minter):
    return await minter.purchase("0x02a1c9babc92d600818ea11ba5b9547f7f25887c", value_to_send=0.000777)


async def mint_8(minter):
    return await minter.purchase("0xcdc9c8060c7c357ee25cd80455cbe05b226d291f", value_to_send=0.000778)


async def mint_9(minter):
    return await minter.purchase("0x706bafabdd00ceac5b66600901a2b1d1f4992b9d", value_to_send=0.000777)


@dp.message_handler(Text(equals="🐳 LFG!"), state=UserFollowing.tap_to_earn)
async def start_earn(message: types.Message, state: FSMContext):
    data = await state.get_data()
    is_ready = data.get("is_ready")

    if is_ready == 0:
        is_ready = -1
        await state.update_data(is_ready=is_ready)

        private_keys = list(data.get("private_keys"))

        await state.update_data(stop_flag=False)

        count_private_keys = len(private_keys)

        final_statistic = "\n📊 <b>Statistic</b> \n\n"

        wait_message = await message.answer("Taking off ✈️...")

        minters_obj = [Minter(private_key) for private_key in private_keys]

        ########################################### BRIDGE  ###########################################

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        bridgers_obj = [Bridger(private_key) for private_key in private_keys]
        bridge_data = await state.get_data()
        bridge_amount = list(bridge_data.get("random_amount"))

        bridgers_counter = 1
        bridgers_result_list = []

        for bridgers, random_amount in zip(bridgers_obj, bridge_amount):
            is_used_bridge = await Bridger.used_bridge(bridgers.pk)
            if is_used_bridge:
                bridgers_result_list.append("[BRIDGED]")
            else:
                result_of_bridge = await bridgers.eth_zora_bridge(random_amount)
                bridgers_result_list.append(result_of_bridge)
                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"⏳ Bridge {bridgers_counter}/{count_private_keys}")
                user_data = await state.get_data()
                if user_data.get("stop_flag"):
                    return

                bridgers_counter += 1
                await asyncio.sleep(Randomiser.random_bridge())

        bridge_statistic = "📊 Statistic \n\n" \
                           " # Bridge (ETH Mainnet —> Zora Mainnet)  \n"

        final_statistic += "\n <u> Bridge (ETH Mainnet —> Zora Mainnet) </u> \n"

        for i in range(len(bridgers_result_list)):
            final_statistic += f"Wallet {i + 1}: {bridgers_result_list[i]} \n"
            bridge_statistic += f"Wallet {i + 1}: {bridgers_result_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        #############################################################################################

        sleep_on_0 = Randomiser.random_bridge_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=bridge_statistic + f"\n Sleeping on {sleep_on_0} sec ...")
        await asyncio.sleep(sleep_on_0)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        ########################################## CONTRACT  ###########################################

        random_names = list(animals.animals.keys())
        random_symbols = list(animals.animals.values())
        random_desc = list(desc_list.description)

        random.shuffle(random_names)
        random.shuffle(random_symbols)
        random.shuffle(random_desc)

        random_names = random_names[:count_private_keys]
        random_symbols = random_symbols[:count_private_keys]
        random_desc = random_desc[:count_private_keys]

        mintPrice_list = [Randomiser.mintPrice() for _ in range(count_private_keys)]
        mintLimitPerAddress_list = [Randomiser.mintLimitPerAddress() for _ in range(count_private_keys)]
        editionSize_list = [Randomiser.editionSize() for _ in range(count_private_keys)]
        royaltyBPS_list = [Randomiser.royaltyBPS() for _ in range(count_private_keys)]
        imageURI_list = []

        for elem in imageURI_list_hashes:
            imageURI_list.append("ipfs://" + elem)
        random.shuffle(imageURI_list)

        contract_counter = 1
        list_of_contract_result = []
        final_statistic += "\n <u> NFT create </u> \n"
        wait_message_text = "📊 Statistic \n\n" \
                            " NFT create \n"

        for minter, name, symbol, description, mintPrice, \
            mintLimitPerAddress, editionSize, royaltyBPS, imageURI in zip(minters_obj, random_names, random_symbols,
                                                                          random_desc,
                                                                          mintPrice_list, mintLimitPerAddress_list,
                                                                          editionSize_list, royaltyBPS_list, imageURI_list):
            result = await minter.createERC721(name=name, symbol=symbol, description=description, mintPrice=mintPrice,
                                               mintLimitPerAddress=mintLimitPerAddress,
                                               editionSize=editionSize, royaltyBPS=royaltyBPS, imageURI=imageURI)
            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            list_of_contract_result.append(result)
            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Creating ERC721 {contract_counter}/{count_private_keys}")
            contract_counter += 1

            await asyncio.sleep(Randomiser.random_contract())

        for i in range(len(list_of_contract_result)):
            final_statistic += f"Wallet {i + 1}: {list_of_contract_result[i]} \n"
            wait_message_text += f"Wallet {i + 1}: {list_of_contract_result[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        #############################################################################################

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        sleep_on_1 = Randomiser.random_contract_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=wait_message_text + f"\nSleeping on {sleep_on_1} sec ...")
        await asyncio.sleep(sleep_on_1)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        ########################################## WARM UP  ###########################################

        warm_up_statistic = "📊 Statistic \n\n" \
                            " Warm Up #1 \n"

        final_statistic += "\n <u> Warm Up #1 </u> \n"

        # 1
        warm_up_counter_1 = 1
        warm_up_result_1_list = []
        for minter in minters_obj:
            result1 = await minter.walletWarmUp1(minter.collectionAddress, Minter.generateUri())
            warm_up_result_1_list.append(result1)
            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Warm up #1  {warm_up_counter_1}/{count_private_keys}")
            warm_up_counter_1 += 1

            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_warm_up())

        for i in range(len(warm_up_result_1_list)):
            final_statistic += f"Wallet {i + 1}: {warm_up_result_1_list[i]} \n"
            warm_up_statistic += f"Wallet {i + 1}: {warm_up_result_1_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        sleep_on_warm_up_1 = Randomiser.random_warm_up_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=warm_up_statistic + f"\nSleeping on {sleep_on_warm_up_1} sec ...")
        await asyncio.sleep(sleep_on_warm_up_1)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        # 2
        warm_up_statistic += "\n Warm Up #2 \n"
        final_statistic += "\n <u> Warm Up #2 </u> \n"

        warm_up_counter_2 = 1
        warm_up_result_2_list = []
        for minter in minters_obj:
            result2 = await minter.walletWarmUp2(minter.collectionAddress, round(random.uniform(0.00001, 150), 5))
            warm_up_result_2_list.append(result2)
            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Warm up #2  {warm_up_counter_2}/{count_private_keys}")
            warm_up_counter_2 += 1
            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_warm_up())

        for i in range(len(warm_up_result_2_list)):
            final_statistic += f"Wallet {i + 1}: {warm_up_result_2_list[i]} \n"
            warm_up_statistic += f"Wallet {i + 1}: {warm_up_result_2_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        sleep_on_warm_up_2 = Randomiser.random_warm_up_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=warm_up_statistic + f"\nSleeping on {sleep_on_warm_up_2} sec ...")
        await asyncio.sleep(sleep_on_warm_up_2)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        # 3
        warm_up_statistic += "\n Warm Up #3 \n"
        final_statistic += "\n <u> Warm Up #3 </u> \n"

        warm_up_counter_3 = 1
        warm_up_result_3_list = []
        for minter in minters_obj:
            result3 = await minter.walletWarmUp2(minter.collectionAddress, round(random.uniform(0.00001, 150), 5))
            warm_up_result_3_list.append(result3)
            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Warm up #3  {warm_up_counter_3}/{count_private_keys}")
            warm_up_counter_3 += 1

            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_warm_up())

        for i in range(len(warm_up_result_3_list)):
            final_statistic += f"Wallet {i + 1}: {warm_up_result_3_list[i]} \n"
            warm_up_statistic += f"Wallet {i + 1}: {warm_up_result_3_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        #############################################################################################

        sleep_on_warm_up_3 = Randomiser.random_warm_up_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=warm_up_statistic + f"\nSleeping on {sleep_on_warm_up_3} sec ...")
        await asyncio.sleep(sleep_on_warm_up_3)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        ########################################### MINTS  ###########################################

        mints_func = [mint_1, mint_2, mint_3, mint_4, mint_5, mint_6, mint_7, mint_8, mint_9]
        minters_obj_for_mint = [Minter(private_key) for private_key in private_keys]
        used_functions_by_minters = {minter: [] for minter in minters_obj_for_mint}

        # 1
        mint_statistic = "📊 Statistic \n\n" \
                         " Mint #1 \n"

        final_statistic += "\n <u> Mint #1 </u> \n"

        mint_1_counter = 1
        mint_1_result_list = []

        random.shuffle(mints_func)

        for minter in minters_obj_for_mint:
            while mints_func[0] in used_functions_by_minters[minter]:
                random.shuffle(mints_func)

            used_functions_by_minters[minter].append(mints_func[0])

            mint_1_result = await mints_func[0](minter)

            if mint_1_result is None:
                mint_1_result = "❌ Something went wrong"

            mint_1_result_list.append(mint_1_result)
            random.shuffle(mints_func)

            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Mint #1  {mint_1_counter}/{count_private_keys}")
            mint_1_counter += 1

            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_mint())

        for i in range(len(mint_1_result_list)):
            final_statistic += f"Wallet {i + 1}: {mint_1_result_list[i]} \n"
            mint_statistic += f"Wallet {i + 1}: {mint_1_result_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        sleep_on = Randomiser.random_mint_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
        await asyncio.sleep(sleep_on)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        # 2
        mint_statistic += "\n Mint #2 \n"
        final_statistic += "\n <u> Mint #2 </u> \n"

        mint_2_counter = 1
        mint_2_result_list = []
        for minter in minters_obj_for_mint:
            while mints_func[1] in used_functions_by_minters[minter]:
                random.shuffle(mints_func)
            used_functions_by_minters[minter].append(mints_func[1])

            mint_2_result = await mints_func[1](minter)

            if mint_2_result is None:
                mint_2_result = "❌ Something went wrong"

            mint_2_result_list.append(mint_2_result)
            random.shuffle(mints_func)
            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Mint #2  {mint_2_counter}/{count_private_keys}")
            mint_2_counter += 1

            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_mint())

        for i in range(len(mint_2_result_list)):
            final_statistic += f"Wallet {i + 1}: {mint_2_result_list[i]} \n"
            mint_statistic += f"Wallet {i + 1}: {mint_2_result_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        sleep_on = Randomiser.random_mint_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
        await asyncio.sleep(sleep_on)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        # 3
        mint_statistic += "\n Mint #3 \n"
        final_statistic += "\n <u> Mint #3 </u> \n"

        mint_3_counter = 1
        mint_3_result_list = []
        for minter in minters_obj_for_mint:
            while mints_func[2] in used_functions_by_minters[minter]:
                random.shuffle(mints_func)
            used_functions_by_minters[minter].append(mints_func[2])

            mint_3_result = await mints_func[2](minter)

            if mint_3_result is None:
                mint_3_result = "❌ Something went wrong"
            mint_3_result_list.append(mint_3_result)
            random.shuffle(mints_func)
            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Mint #3  {mint_3_counter}/{count_private_keys}")
            mint_3_counter += 1

            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_mint())

        for i in range(len(mint_3_result_list)):
            final_statistic += f"Wallet {i + 1}: {mint_3_result_list[i]} \n"
            mint_statistic += f"Wallet {i + 1}: {mint_3_result_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        sleep_on = Randomiser.random_mint_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
        await asyncio.sleep(sleep_on)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        # 4
        mint_statistic += "\n Mint #4 \n"
        final_statistic += "\n <u> Mint #4 </u> \n"

        mint_4_counter = 1
        mint_4_result_list = []

        for minter in minters_obj_for_mint:
            while mints_func[3] in used_functions_by_minters[minter]:
                random.shuffle(mints_func)
            used_functions_by_minters[minter].append(mints_func[3])

            mint_4_result = await mints_func[3](minter)

            if mint_4_result is None:
                mint_4_result = "❌ Something went wrong"

            mint_4_result_list.append(mint_4_result)
            random.shuffle(mints_func)

            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Mint #4  {mint_4_counter}/{count_private_keys}")
            mint_4_counter += 1

            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_mint())

        for i in range(len(mint_4_result_list)):
            final_statistic += f"Wallet {i + 1}: {mint_4_result_list[i]} \n"
            mint_statistic += f"Wallet {i + 1}: {mint_4_result_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        sleep_on = Randomiser.random_mint_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
        await asyncio.sleep(sleep_on)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        # 5
        mint_statistic += "\n Mint #5 \n"
        final_statistic += "\n <u> Mint #5 </u> \n"

        mint_5_counter = 1
        mint_5_result_list = []

        for minter in minters_obj_for_mint:
            while mints_func[4] in used_functions_by_minters[minter]:
                random.shuffle(mints_func)
            used_functions_by_minters[minter].append(mints_func[4])

            mint_5_result = await mints_func[4](minter)

            if mint_5_result is None:
                mint_5_result = "❌ Something went wrong"

            mint_5_result_list.append(mint_5_result)
            random.shuffle(mints_func)

            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Mint #5  {mint_5_counter}/{count_private_keys}")
            mint_5_counter += 1

            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_mint())

        for i in range(len(mint_5_result_list)):
            final_statistic += f"Wallet {i + 1}: {mint_5_result_list[i]} \n"
            mint_statistic += f"Wallet {i + 1}: {mint_5_result_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        sleep_on = Randomiser.random_mint_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
        await asyncio.sleep(sleep_on)
        user_data = await state.get_data()

        if user_data.get("stop_flag"):
            return

        # 6
        mint_statistic += "\n Mint #6 \n"
        final_statistic += "\n <u> Mint #6 </u> \n"

        mint_6_counter = 1
        mint_6_result_list = []

        for minter in minters_obj_for_mint:
            while mints_func[5] in used_functions_by_minters[minter]:
                random.shuffle(mints_func)
            used_functions_by_minters[minter].append(mints_func[5])

            mint_6_result = await mints_func[5](minter)

            if mint_6_result is None:
                mint_6_result = "❌ Something went wrong"

            mint_6_result_list.append(mint_6_result)
            random.shuffle(mints_func)

            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Mint #6  {mint_6_counter}/{count_private_keys}")
            mint_6_counter += 1

            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_mint())

        for i in range(len(mint_6_result_list)):
            final_statistic += f"Wallet {i + 1}: {mint_6_result_list[i]} \n"
            mint_statistic += f"Wallet {i + 1}: {mint_6_result_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        sleep_on = Randomiser.random_mint_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
        await asyncio.sleep(sleep_on)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        # 7
        mint_statistic += "\n Mint #7 \n"
        final_statistic += "\n <u> Mint #7 </u> \n"

        mint_7_counter = 1
        mint_7_result_list = []

        for minter in minters_obj_for_mint:
            while mints_func[6] in used_functions_by_minters[minter]:
                random.shuffle(mints_func)
            used_functions_by_minters[minter].append(mints_func[6])

            mint_7_result = await mints_func[6](minter)

            if mint_7_result is None:
                mint_7_result = "❌ Something went wrong"

            mint_7_result_list.append(mint_7_result)
            random.shuffle(mints_func)

            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Mint #7  {mint_7_counter}/{count_private_keys}")
            mint_7_counter += 1

            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_mint())

        for i in range(len(mint_7_result_list)):
            final_statistic += f"Wallet {i + 1}: {mint_7_result_list[i]} \n"
            mint_statistic += f"Wallet {i + 1}: {mint_7_result_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        sleep_on = Randomiser.random_mint_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
        await asyncio.sleep(sleep_on)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        # 8
        mint_statistic += "\n Mint #8 \n"
        final_statistic += "\n <u> Mint #8 </u> \n"

        mint_8_counter = 1
        mint_8_result_list = []
        for minter in minters_obj_for_mint:
            while mints_func[7] in used_functions_by_minters[minter]:
                random.shuffle(mints_func)
            used_functions_by_minters[minter].append(mints_func[7])

            mint_8_result = await mints_func[7](minter)

            if mint_8_result is None:
                mint_8_result = "❌ Something went wrong"

            mint_8_result_list.append(mint_8_result)
            random.shuffle(mints_func)

            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Mint #8  {mint_8_counter}/{count_private_keys}")
            mint_8_counter += 1

            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_mint())

        for i in range(len(mint_8_result_list)):
            final_statistic += f"Wallet {i + 1}: {mint_8_result_list[i]} \n"
            mint_statistic += f"Wallet {i + 1}: {mint_8_result_list[i]} \n"

        await state.update_data(final_statistic=final_statistic)

        sleep_on = Randomiser.random_mint_after()
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=mint_statistic + f"\n Sleeping on {sleep_on} sec ...")
        await asyncio.sleep(sleep_on)

        user_data = await state.get_data()
        if user_data.get("stop_flag"):
            return

        # 9
        mint_statistic += "\n Mint #9 \n"
        final_statistic += "\n <u> Mint #9 </u> \n"

        mint_9_counter = 1
        mint_9_result_list = []

        for minter in minters_obj_for_mint:
            while mints_func[8] in used_functions_by_minters[minter]:
                random.shuffle(mints_func)
            used_functions_by_minters[minter].append(mints_func[8])

            mint_9_result = await mints_func[8](minter)

            logger.info(f"🔉 List used_functions_by_minters: {used_functions_by_minters[minter]}")

            if mint_9_result is None:
                mint_9_result = "❌ Something went wrong"

            mint_9_result_list.append(mint_9_result)
            random.shuffle(mints_func)

            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Mint #9  {mint_9_counter}/{count_private_keys}")
            mint_9_counter += 1

            user_data = await state.get_data()
            if user_data.get("stop_flag"):
                return

            await asyncio.sleep(Randomiser.random_mint())

        for i in range(len(mint_9_result_list)):
            final_statistic += f"Wallet {i + 1}: {mint_9_result_list[i]} \n"
            mint_statistic += f"Wallet {i + 1}: {mint_9_result_list[i]} \n"

        is_ready_to_start = 0
        await state.update_data(final_statistic=final_statistic)
        await state.update_data(is_ready_to_start=is_ready_to_start)

        await bot.delete_message(chat_id=wait_message.chat.id,
                                 message_id=wait_message.message_id)

        buttons = [
            KeyboardButton(text="⬅ Go to menu"),
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                           resize_keyboard=True)
        is_ready = 0
        await state.update_data(is_ready=is_ready)
        await UserFollowing.wallet_menu.set()
        await message.answer(final_statistic,
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