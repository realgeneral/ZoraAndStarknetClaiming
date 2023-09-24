from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton("🗺 How to start?")
b2 = KeyboardButton("🧐 What can bot do?")
b3 = KeyboardButton("⛽️ What is GWEI ?")
b4 = KeyboardButton("💎 Premium version")
b5 = KeyboardButton("⬅ Go to menu")

faq_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
faq_buttons.row(b1, b2).row(b3, b4).row(b5)
