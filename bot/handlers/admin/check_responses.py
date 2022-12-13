from aiogram import types
from aiogram.dispatcher.filters import Text
from database import sql_get_all_questionnaires_titles, sql_get_responses
from loader import dp, bot
from inline import generate_inline
from utils import get_response_as_excel
from aiogram.types import InputFile


@dp.message_handler(Text(equals=['Переглянути відповіді']))
async def get_quests(message : types.Message):
    await message.answer('Оберіть опитування для перегляду результатів', reply_markup=generate_inline(sql_get_all_questionnaires_titles(), 'Перевірити '))


@dp.callback_query_handler(Text(startswith='Перевірити '))
async def get_results(message : types.CallbackQuery):
    quest_jsons = sql_get_responses(message.data.replace('Перевірити ', ''))
    await bot.send_document(message.from_user.id, ('resposes.xlsx', get_response_as_excel(quest_jsons) ))
