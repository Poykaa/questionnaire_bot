from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(token='5835720673:AAHHGZDZe9SR43uGmpBB7K05XBACK4eUhzw')
dp = Dispatcher(bot=bot, storage=storage)
