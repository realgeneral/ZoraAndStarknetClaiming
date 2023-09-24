import asyncio

import httpx

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.utils.Estimate import Estimate
from app.logs.log import logging as logger


async def get_usd_balance(url, eth_amount):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'ethereum' in data and 'usd' in data['ethereum']:
                eth_to_usd = data['ethereum']['usd']
                usd_amount = float(eth_amount) * eth_to_usd
                return round(usd_amount, 2)
            else:
                logger.error(f"{response.url} --- NO ETH or USD")
                return "-"
        else:
            logger.error(f"{response.url} --- CODE: {response.status_code}")
            return "-"
    except Exception as err:
        logger.error(f"Something went wrong: {err}")
        return "-"


@dp.message_handler(Text(equals=["👝 Check balance"]), state=UserFollowing.choose_point)
async def check_wallet_keys(message: types.Message, state: FSMContext):
    url_eth = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

    data = await state.get_data()
    private_keys = data.get("private_keys")
    bridge_amount = list(data.get("random_amount"))

    reply_message = "👝 Check balance \n\n"
    wait_message = await message.answer("⏳ Getting information about wallets ...")

    for i, random_amount in zip(range(len(private_keys)), bridge_amount):
        es = Estimate(private_keys[i])
        reply_message += f"*{es.get_eth_address()}* \n\n"

        eth_balance = es.get_eth_balance()
        zora_balance = es.get_zora_balance()

        eth_required = es.eth_required(random_amount)

        if eth_balance != "-":
            usd_amount = await get_usd_balance(url_eth, eth_balance)
        else:
            usd_amount = "-"

        if zora_balance != "-":
            usd_zora_amount = await get_usd_balance(url_eth, zora_balance)
        else:
            usd_zora_amount = "-"

        usd_required = await get_usd_balance(url_eth, eth_required)

        reply_message += f"*ETH balance:* {eth_balance} (= {usd_amount} USD) \n"
        reply_message += f"*Zora balance:* {zora_balance} (= {usd_zora_amount} USD) \n"
        if eth_balance != "-":
            if eth_balance >= eth_required:
                    reply_message += "✅ \n\n\n"
            else:
                    reply_message += f"*ETH required:* {round(eth_required, 5)} (= {usd_required} USD) \n"
                    reply_message += f"❌ not enough ETH to do all activities \n\n\n"

        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Getting information about wallets {i + 1}/{len(private_keys)}")
        await asyncio.sleep(1)

    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await bot.delete_message(chat_id=wait_message.chat.id,
                             message_id=wait_message.message_id)
    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.HTML,
                         reply_markup=reply_markup)
