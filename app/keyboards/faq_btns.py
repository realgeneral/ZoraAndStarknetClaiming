from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

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

# faq_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
# faq_buttons.row(b1, b2).row(b3, b4).row(b6, b7).row(b9, b10).row(b8, b5)

faq_buttons = InlineKeyboardMarkup()
btn_1 = InlineKeyboardButton("📍 Expected $ from StarkNet/Zora?", callback_data="faq_1")
btn_2 = InlineKeyboardButton("📍 How to not become Sybil?", callback_data="faq_2")
btn_3 = InlineKeyboardButton("📍 StarkNet wallet cost", callback_data="faq_3")
btn_4 = InlineKeyboardButton("📍 Zora wallet cost", callback_data="faq_4")
btn_5 = InlineKeyboardButton("📍 Data privacy concerns?", callback_data="faq_5")
btn_6 = InlineKeyboardButton("📍 How to deploy StarkNet wallet?", callback_data="faq_6")
btn_7 = InlineKeyboardButton("📍 How to load up data for Zora?", callback_data="faq_7")
btn_8 = InlineKeyboardButton("📍 How to load up data for StarkNet?", callback_data="faq_8")
btn_9 = InlineKeyboardButton("⬅ Go to menu", callback_data="faq_0")

faq_buttons.add(btn_1).add(btn_2).add(btn_3).add(btn_4).add(btn_5).add(btn_6).add(btn_7).add(btn_8).add(btn_9)