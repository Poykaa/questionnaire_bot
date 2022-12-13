from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from config import admins
from keyboards import main_admin_kb, main_user_kb
from database import sql_new_user


@dp.message_handler(CommandStart())
async def start(message : types.Message):
    sql_new_user(message.from_user)
    if message.from_user.id in admins:
        await message.answer('''Вас вітає єдиний і кращий Telegram бот для проведення опитувань! Щоб створити або пройти опитування оберіть потрібний пункт!''', reply_markup=main_admin_kb)
    else:
        await message.answer('''Вас вітає єдиний і кращий Telegram бот для проведення опитувань! Щоб пройти опитування оберіть потрібний пункт!''', reply_markup=main_user_kb)