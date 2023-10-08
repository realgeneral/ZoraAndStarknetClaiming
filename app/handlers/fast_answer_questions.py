from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InputFile, \
    InlineKeyboardMarkup

from app.create_bot import dp, bot
from app.handlers.main_menu import send_menu
from app.states import UserFollowing
from app.keyboards import faq_buttons


@dp.message_handler(Text(equals=["ℹ️ FAQ"]), state='*')
async def faq_handler(message: types.Message):
    reply_message_1 = "ℹ️ <b>FAQ</b> "
    reply_message_2 = "<i>Choose your question and hit that button on the menu below!</i>"

    await UserFollowing.choose_faq.set()
    await message.answer(reply_message_1, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=ReplyKeyboardRemove())

    await message.answer(reply_message_2, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=faq_buttons)


@dp.callback_query_handler(lambda query: query.data.startswith('faq_'), state=UserFollowing.choose_faq)
async def process_faq_callback(callback_query: types.CallbackQuery, state: FSMContext):
    faq_amount = int(callback_query.data.split('_')[1])

    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id, message_id)

    if faq_amount == 0:
        callback_query.message.from_user.id = callback_query.from_user.id
        await UserFollowing.wallet_menu.set()
        await send_menu(callback_query.message, state)
        return

    path_to_file = ""
    reply_message = ""

    if faq_amount == 1:
        reply_message = "📍 <b>How much $ is expected from StarkNet/Zora? </b> \n\n" \
                        "Historically, web3 users have earned $550/wallet from similar airdrops." \
                        " Expect $350-$800 per project per wallet. For two projects: roughly $1000/wallet"
    elif faq_amount == 2:
        reply_message = "📍 <b>How to not become Sybil?</b> \n\n" \
                        "🔒 Don't link your wallets\n" \
                        "🚫 Don't bail on your wallets after you've been active in a project\n" \
                        "🔥 Warm up your wallets\n "
    elif faq_amount == 3:
        reply_message = "📍 <b>What is the cost per wallet for StarkNet?</b> \n\n" \
                        "💼 Deposit: <i>0.0215 eth ($35)</i>\n" \
                        "💰 Post-activity balance: <i>0.02 eth ($32)</i>\n" \
                        "🤖 Wallet run: <i>$5</i>\n" \
                        "💵 Total: <i>$7</i>\n" \
                        "💸 Potential Profit: <i>$550</i>\n"
    elif faq_amount == 4:
        reply_message = "📍 <b>What is the cost per wallet for Zora?</b>\n\n" \
                        "💼 Deposit: <i>0.01 eth ($18)</i>\n" \
                        "💰 Post-activity balance: <i>0.005 eth ($9)</i>\n" \
                        "🤖 Wallet run: <i>$5</i>\n" \
                        "💵 Total: <i>$14</i>\n" \
                        "💸 Potential Profit: <i>$680</i>\n"
    elif faq_amount == 5:
        reply_message = "📍 <b>Concerned about your personal data?</b>\n\n" \
                        '🔐 Using a wallet requires a private key. Your funds are protected. Our bot uses "disposable states," not storing data post-session.\n' \
                        '💌 Reach out for more info: @ebsh_web3_support\n'
    elif faq_amount == 6:
        reply_message = "📍 <b>How to deploy StarkNet wallet?</b>"
        path_to_file = "app/data/deploy_video.mp4"
    elif faq_amount == 7:
        reply_message = "📍 <b>How can I load my data for Zora?</b>"
        path_to_file = "app/data/metamask.mp4"
    elif faq_amount == 8:
        reply_message = "📍 <b>How can I load my data for StarkNet?</b>"
        path_to_file = "app/data/argentx.mp4"

    go_back_keyboard = InlineKeyboardMarkup()
    btn_go_back = InlineKeyboardButton("⬅ Go back", callback_data="go_back")
    go_back_keyboard.add(btn_go_back)

    if path_to_file:
        await bot.send_animation(callback_query.from_user.id, InputFile(path_to_file),
                                 caption=reply_message,
                                 parse_mode=types.ParseMode.HTML,
                                 reply_markup=go_back_keyboard)
    else:
        await bot.send_message(callback_query.from_user.id,
                               reply_message,
                               parse_mode=types.ParseMode.HTML,
                               reply_markup=go_back_keyboard)


@dp.callback_query_handler(lambda c: c.data == "go_back", state=UserFollowing.choose_faq)
async def go_back_to_faq(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    await bot.delete_message(chat_id, message_id)

    callback_query.message.from_user.id = callback_query.from_user.id
    await faq_handler(callback_query.message)


