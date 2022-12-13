from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_inline(lst, callback, last=''):
    base_menu = InlineKeyboardMarkup()
    for item in lst:
        item = str(item).strip("('',)")
        base_menu.insert(InlineKeyboardButton(text=item, callback_data=f'{callback}{item}'))
    if last:
        base_menu.insert(InlineKeyboardButton(text=last, callback_data=last))
    return base_menu