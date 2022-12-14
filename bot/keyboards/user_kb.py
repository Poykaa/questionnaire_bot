from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

cancel_button = KeyboardButton(text='Відмінити')

main_user_kb = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Пройти опитування'),
    KeyboardButton(text='Доєднатись до групи')
]], resize_keyboard=True)
