from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from data import DataBase

def admin_panel() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Новый учитель', callback_data='new_teacher')
    return builder.as_markup()

def nicho() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Ничо', callback_data='/nicho')
    return builder.as_markup()