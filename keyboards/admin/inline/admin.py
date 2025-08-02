from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from data import DataBase

def admin_panel() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Панель', callback_data='/panel')
    return builder.as_markup()

def nicho() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Ничо', callback_data='/nicho')
    return builder.as_markup()