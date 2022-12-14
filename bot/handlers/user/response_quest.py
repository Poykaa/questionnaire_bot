from aiogram import types
from states import QuestPassage
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database import sql_get_questionnaire, sql_get_allowed_questionnaires, sql_write_resopnse, sql_get_username
from inline import generate_inline
from keyboards import main_user_kb, main_admin_kb
from config import admins


async def next_question(message, state):
    async with state.proxy() as data:
        k = tuple(data['responses'][-1].keys())[0]
        data['responses'][-1][k] = message.text if type(message) is types.Message else message.data
    async with state.proxy() as data:
        try:
            q = tuple(data['questions']['questions'][len(data['responses'])].items())[0]
        except IndexError:
            async with state.proxy() as data:
                sql_write_resopnse(data, message.from_user)
            await state.finish()
            await bot.send_message(message.from_user.id, 'Опитуавання завершено, відповіді збережено.', reply_markup=main_admin_kb if message.from_user.id in admins else main_user_kb)
            return
        data['responses'].append({q[0]: ''})
        if q[1]:
            # Если в вопросе варианты ответа
            await bot.send_message(message.from_user.id, q[0], reply_markup=generate_inline(q[1], ''))
        else:
            await bot.send_message(message.from_user.id, q[0])

#команда для старта опроса
@dp.message_handler(Text(startswith='Пройти опитування'))
async def start_quest(message : types.Message):
    quests = sql_get_allowed_questionnaires(message.from_user.id)
    if not quests:
        await message.answer('У вас не має відкритих опитуваннь')
        return
    await QuestPassage.initial.set()
    k = generate_inline(quests, 'start', 'Відмінити')
    await message.answer('Оберіть опитування для проходження', reply_markup=k)


@dp.callback_query_handler(Text(equals=['Відмінити']), state=QuestPassage.initial)
async def cancel(message : types.CallbackQuery, state : FSMContext):
    await state.finish()
    await message.answer('Відмінено')
    await message.message.delete()


@dp.callback_query_handler(Text(startswith='start'), state=QuestPassage.initial)
async def initial_question(message : types.CallbackQuery, state : FSMContext):
    async with state.proxy() as data:
        data['user'] = sql_get_username(message.from_user.id)
        data['responses'] = []
        data['questions'] = sql_get_questionnaire(message.data.replace('start', ''))
        q = tuple(data['questions']['questions'][0].items())[0]
        data['responses'].append({q[0]: ''})
        if q[1]:
            # Если в вопросе варианты ответа
            await bot.send_message(message.from_user.id, 'Оберіть відповідь', reply_markup=generate_inline(q[1], ''))
        else:
            await bot.send_message(message.from_user.id, q[0])
    await QuestPassage.next()

@dp.message_handler(state=QuestPassage.question)
async def next_handler(message : types.Message, state : FSMContext):
    await next_question(message, state)


@dp.callback_query_handler(state=QuestPassage.question)
async def next_callback(message : types.CallbackQuery, state : FSMContext):
    await next_question(message, state)