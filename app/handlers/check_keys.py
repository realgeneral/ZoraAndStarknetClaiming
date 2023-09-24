from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp
from app.states import UserFollowing


@dp.message_handler(Text(equals=["🔑 Check keys"]), state=UserFollowing.choose_point)
async def check_private_keys(message: types.Message, state: FSMContext):
    print("Zashel")
    data = await state.get_data()
    private_keys = list(data.get("private_keys"))
    count_private_keys = len(private_keys)

    message_response = ""
    for i in range(count_private_keys):
        message_response += f"{i+1}. *{private_keys[i][0:6]}...{private_keys[i][-4:]}* \n"

    await UserFollowing.choose_point.set()
    await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN)

