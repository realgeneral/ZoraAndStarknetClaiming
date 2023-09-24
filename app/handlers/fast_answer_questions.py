import asyncio

import httpx

from aiogram import types
from aiogram.dispatcher.filters import Text

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.keyboards import faq_buttons


@dp.message_handler(Text(equals=["ℹ️ FAQ"]), state='*')
async def faq_handler(message: types.Message):
    reply_message = "ℹ️ FAQ \n\n" \
                    "Choose your question and hit that button on the menu below!"

    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=faq_buttons)


@dp.message_handler(Text(equals=["🧐 What can bot do?"]), state=UserFollowing.choose_point)
async def what_can_bot_do(message: types.Message):
    reply_message = "*Bot's superpowers: * \n \n" \
                    "• 📩 Bridge to Zora Mainnet from ETH Mainnet \n\n" \
                    "• 🀄️ Create NFTs  \n\n" \
                    "• 🖼 Mint important NFTs (updated list)  \n\n" \
                    "• 🏋️‍♂️ Wallet warm-up (simulation of real human actions)  \n\n" \
                    "• ⛽️ GWEI downgrade mode - literally lowers the fees to zero \n\n"

    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=faq_buttons)


@dp.message_handler(Text(equals=["⛽️ What is GWEI ?"]), state=UserFollowing.choose_point)
async def what_can_bot_do(message: types.Message):
    reply_message = "*What is GWEI?* \n\n" \
                    '*GWEI* -  is a unit of payment for "*gas*", which is the fee required to make transactions or ' \
                    " ⛽️ Gas in Ethereum can be like the fuel for a car. \n\n" \
                    '🚘 Just as a *car* needs fuel to run, transactions and smart contracts in Ethereum require "*gas*" to operate.   \n\n' \
                    '⛽️ *GWEI* is similar to the quantification of fuel in liters or gallons - it\'s a unit of measurement for "*gas*".   \n\n' \
                    "💸 The higher the *GWEI*, the higher the *transaction fee*.  \n\n" \
                    "🔎 *To check the current GWEI tap on «⛽️Check GWEI» button in the main menu.* \n\n"

    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=faq_buttons)


@dp.message_handler(Text(equals=["💎 Premium version"]), state=UserFollowing.choose_point)
async def premium_version(message: types.Message):
    reply_message = "<b>Premium version</b>\n\n" \
                    "To set-up more wallets in the bot, you need to become a premium memeber.  \n\n" \
                    "<i>- The ability to load up to 10 wallets into the bot </i>\n" \
                    "<i>- Be among the first to get access to our latest developments</i>\n"\
                    "<i>- Your tasks bot will perform in high priority </i>\n" \
                    "<i>- You will give us the motivation to make the software even better for you</i>\n\n" \
                    "<b> <a href='https://t.me/whatheshark'>DM</a> for price</b>\n"

    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.HTML,
                         reply_markup=faq_buttons)


@dp.message_handler(Text(equals=["🗺 How to start?"]), state=UserFollowing.choose_point)
async def premium_version(message: types.Message):
    reply_message = "<b> How to start? </b>\n\n" \
                    '1. Load-up your private keys by pressing <b>«➕ Load new wallets»</b> button in the menu.\n' \
                    '  [<a href="https://support.metamask.io/hc/en-us/articles/360015289632-How-to-export-an-account-s-private-key">guide</a>]\n\n' \
                    '<b>Example:</b>\n' \
                    '<i>a692b7245354c12ca7ef7138bfdc040abc7d07612c9f3770c9be81d9459911ca</i>\n' \
                    '<i>8cd22cacf476cd9ffebbbe05877c9cab695c6abafcad010a0194dbb1cb6e66f1</i>\n' \
                    '<i>0b77a1a6618f75360f318e859a89ba8008b8d0ceb10294418443dc8fd643e6bb</i>\n\n' \
                    '2. Withdraw the required amount of ETH in <b>Ethereum Mainnet Chain</b> to your wallet using CEX (<b>Binance, OKX,</b> etc).\n\n' \
                    '3. After that go to the main menu and press <b>«💸 Start script» </b> button.' \

    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.HTML,
                         reply_markup=faq_buttons)