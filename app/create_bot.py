import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_TOKEN = "6403780572:AAGz43fjxC8oBcr2OVOqagjx6BaRS1x8psQ"

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
