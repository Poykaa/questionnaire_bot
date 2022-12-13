from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

cancel_button = KeyboardButton(text='Отмена')

main_admin_kb = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Пройти опитування'),
    KeyboardButton(text='Створити опитування'),
    KeyboardButton(text='Додати групу'),
    KeyboardButton(text='Доєднатись до групи'),
    KeyboardButton(text='Переглянути відповіді')
]], resize_keyboard=True)


questionnaire_kb = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Відмінити створення'),
    KeyboardButton(text='Створити'),
]], resize_keyboard=True)

cancel_kb = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Відмінити створення'),
]], resize_keyboard=True)