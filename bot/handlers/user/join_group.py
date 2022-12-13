from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp
from database import sql_join_user_in_group, sql_get_groups
from inline import generate_inline


@dp.message_handler(Text('Доєднатись до групи'))
async def chose_group(message : types.Message):
    groups = sql_get_groups()
    await message.answer('Оберіть потрібну групу', reply_markup=generate_inline(groups, 'JOIN'))


@dp.callback_query_handler(Text(startswith=['JOIN'], ignore_case=True))
async def join_group(message : types.CallbackQuery):
    sql_join_user_in_group(message.from_user.id, message.data.replace('JOIN', ''))