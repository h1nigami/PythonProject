from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

def admin_panel() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Новый учитель', callback_data='new_teacher')
    builder.button(text='Список учителей', callback_data='list_teachers')
    return builder.as_markup()

def teachers(teachers: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for teacher in teachers:
        builder.button(text=f'{teacher.name} {teacher.scores}', callback_data=f'teacher:{teacher.tg_id}')
    builder.button(text='<< Главное меню', callback_data='exit')
    builder.adjust(1)
    return builder.as_markup()

def about(teacher) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Косяк', callback_data=f'misstake:{teacher.tg_id}')
    builder.button(text='Удалить', callback_data=f'delete:{teacher.tg_id}')
    builder.button(text='Добавить группу', callback_data=f'new_group:{teacher.tg_id}')
    builder.button(text='<< Главное меня', callback_data='exit')
    builder.adjust(1)
    return builder.as_markup()

def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='<< Главное меню', callback_data='exit')
    return builder.as_markup()