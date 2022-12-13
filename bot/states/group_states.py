from aiogram.dispatcher.filters.state import StatesGroup, State


class GroupCreator(StatesGroup):
    name = State()
