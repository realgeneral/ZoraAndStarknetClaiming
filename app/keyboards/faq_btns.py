from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton("📍 What does the Zora script include?")
b2 = KeyboardButton("📍 What does the StarkNet script include?")
b3 = KeyboardButton("📍 How much $ is expected from StarkNet/Zora?")
b4 = KeyboardButton("📍 How to not become Sybil?")
b6 = KeyboardButton("📍 What is the cost per wallet for StarkNet? ")
b7 = KeyboardButton("📍 What is the cost per wallet for Zora?")
b8 = KeyboardButton("📍 How to deploy StarkNet wallet?")
b9 = KeyboardButton("📍 How can I load my data for Zora?")
b10 = KeyboardButton("📍 How can I load my data for StarkNet?")


b5 = KeyboardButton("⬅ Go to menu")

faq_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
faq_buttons.row(b1, b2).row(b3, b4).row(b6, b7).row(b9, b10).row(b8, b5)
