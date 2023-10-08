import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_TOKEN = "6303901229:AAEjb4j4jQAt5bXuvK8VML2EhL8pvCWjUic"

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
