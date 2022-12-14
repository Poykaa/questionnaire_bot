from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import main_admin_kb
from loader import dp, bot
from filters import IsAdmin
from states import QuestCreator
from keyboards import questionnaire_kb, cancel_kb, main_admin_kb
from inline import generate_inline
from database import sql_get_groups, sql_create_questionnaire

import re


@dp.message_handler(Text(equals=['Створити опитування'], ignore_case=True), IsAdmin())
async def initial_quest(message : types.Message):
    await QuestCreator.title.set()
    await message.answer('Введіть заголовок опитування', reply_markup=cancel_kb)


@dp.message_handler(Text(equals=['Відмінити створення']), state='*')
async def cancel_quest(message : types.Message, state : FSMContext):
    await state.finish()
    await message.answer('Створення опитування відмінено!', reply_markup=main_admin_kb)


@dp.message_handler(state=QuestCreator.title)
async def set_title(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
        data['groups'] = []
    await QuestCreator.next()
    k = generate_inline(sql_get_groups(), 'Обрати групу №', 'Далі')
    await message.answer('Оберіть групи, які мають пройти опитування (натисніть "Далі", якщо хочете обрати всі групи)', reply_markup=k)


@dp.callback_query_handler(Text(startswith=['Обрати групу №']), state=QuestCreator.select_groups)
async def set_groups(message : types.CallbackQuery, state : FSMContext):
    async with state.proxy() as data:
        data['groups'].append(message.data.replace('Обрати групу №', ''))


@dp.callback_query_handler(Text(equals=['Далі'], ignore_case=True), state=QuestCreator.select_groups)
async def confirm_groups(message : types.CallbackQuery, state : FSMContext):
    await QuestCreator.next()
    await bot.send_message(message.from_user.id, ('''Створіть запитання. Для створення запитання із варіантами відповідей використовуйте конкстукцію: "Запитання ((Варіант відповіді 1/Варіант відповіді 2/ т.д.))'''))



@dp.message_handler(Text(equals=['Створити'], ignore_case=True), state=QuestCreator.question)
async def finish_quest(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        sql_create_questionnaire(data)
    await state.finish()
    await message.answer('Опитування створено!', reply_markup=main_admin_kb)



@dp.message_handler(state=QuestCreator.question)
async def add_question(message : types.Message, state : FSMContext):
    raw = r'\(\(.+\)\)'
    questions = re.search(raw, message.text)
    if questions:
        async with state.proxy() as data:
            data.setdefault('questions', []).append({message.text.replace(questions.group(), '') : questions.group().strip('()').split('/')})
    else:
        async with state.proxy() as data:
            data.setdefault('questions', []).append({message.text : []})
    await message.answer('Введіть ще запитння або завершіть створення', reply_markup=questionnaire_kb)
