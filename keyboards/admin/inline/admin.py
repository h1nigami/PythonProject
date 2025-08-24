from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

def admin_panel() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='👨‍🏫 Новый учитель', callback_data='new_teacher')
    builder.button(text='📋 Список учителей', callback_data='list_teachers')
    builder.adjust(1)
    return builder.as_markup()

def teacher_registration(tg_id: int, username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Да', callback_data=f'registration:{tg_id}:{username}')
    builder.button(text='❌ Нет', callback_data='exit')
    builder.adjust(2)
    return builder.as_markup()

def groups(groups_list: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for group in groups_list:
        builder.button(text=f'👥 {group.name}', callback_data=f'group:{group.id}')
    builder.button(text='🔙 Главное меню', callback_data='exit')
    builder.adjust(1)
    return builder.as_markup()

def teachers(teachers: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for teacher in teachers:
        builder.button(
            text=f'👨‍🏫 {teacher.name} ({teacher.scores} баллов)',
            callback_data=f'teacher:{teacher.tg_id}'
        )
    builder.button(text='🔙 Главное меню', callback_data='exit')
    builder.adjust(1)
    return builder.as_markup()

def about(teacher) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='⚠️ Косяк', callback_data=f'mistake:{teacher.tg_id}')
    builder.button(text='➕ Добавить группу', callback_data=f'new_group:{teacher.tg_id}')
    builder.button(text='➖ Удалить группу', callback_data=f'delete_group:{teacher.tg_id}')
    builder.button(text='✏️ Отредактировать имя', callback_data=f'edit_teacher_name:{teacher.tg_id}')
    builder.button(text='🗑️ Удалить', callback_data=f'delete:{teacher.tg_id}')
    builder.button(text='📊 Статистика', callback_data=f'statistic:{teacher.tg_id}')
    builder.button(text='🔙 Главное меню', callback_data='exit')
    builder.adjust(1)
    return builder.as_markup()

def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='🏠 Главное меню', callback_data='exit')
    return builder.as_markup()