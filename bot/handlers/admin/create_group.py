from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from loader import dp
from states import GroupCreator
from database import sql_create_group
from filters import IsAdmin


@dp.message_handler(Text(equals=['Додати групу'], ignore_case=True), IsAdmin())
async def initial_group(message : types.Message):
    await message.answer('Введіть назву групи')
    await GroupCreator.name.set()


@dp.message_handler(state=GroupCreator.name)
async def create_group(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        sql_create_group(data)
    await state.finish()
    await message.answer('Група успішно створена!')