from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

def admin_panel() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Новый учитель', callback_data='new_teacher')
    builder.button(text='Список учителей', callback_data='list_teachers')
    return builder.as_markup()

def teachers(teachers: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for teacher in teachers:
        builder.button(text=teacher.name, callback_data=str(teacher.tg_id))
    builder.button(text='<< Главное меню', callback_data='exit')
    builder.adjust(1)
    return builder.as_markup()

def nicho() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Ничо', callback_data='/nicho')
    return builder.as_markup()