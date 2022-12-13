from aiogram.dispatcher.filters.state import StatesGroup, State


class QuestCreator(StatesGroup):
    title = State()
    select_groups = State()
    question = State()

class QuestPassage(StatesGroup):
    initial = State()
    question = State()