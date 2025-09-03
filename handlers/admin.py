from aiogram.fsm.context import FSMContext
from data import DataBase, OWNER_ID, PASSWORD
from loader import dp, bot
from permissions import IsAdminCall, IsAdminMessage
from states import AddGroup, AddTeacher, Misstake, EditTeacher
from aiogram import types, F
from keyboards.admin.inline import *
from sqlalchemy import text

db = DataBase()
db.session.execute(text("PRAGMA journal_mode = WAL"))
db.session.execute(text("PRAGMA synchronous=NORMAL"))
db.session.commit()
pending_teachers = dict()


@dp.message(F.text == '/start')
async def handle_start(message: types.Message):
    teacher = db.get_teacher(message.from_user.id)
    if not teacher:
        pending_teachers[message.from_user.id] = {
            'tg_id': message.from_user.id,
            'username': message.from_user.username,
        }
        await message.answer('🔄 Ваш запрос на регистрацию отправлен администратору')
        await bot.send_message(
            chat_id=OWNER_ID,
            text=f'📩 Новый запрос на регистрацию:\n'
                 f'👤 Пользователь: @{message.from_user.username}\n'
                 f'🆔 ID: {message.from_user.id}',
            reply_markup=teacher_registration(
                tg_id=message.from_user.id,
                username=message.from_user.username
            )
        )
    else:
        notes = teacher.notes if teacher.notes else 'отсутствуют'
        await message.answer(
            f"───────────────\n"
            f"👤 <b>Профиль учителя</b>\n"
            f"───────────────\n"
            f"▪️ <b>Имя:</b> {teacher.name}\n"
            f"▪️ 🎯 <b>Баллы:</b> {teacher.scores}\n"
            f"▪️ 📋 <b>Замечания:</b>\n<code>{notes}</code>"
        )


@dp.callback_query(F.data.startswith('registration:'))
async def approve_teacher(callback: types.CallbackQuery):
    _, tg_id, username = callback.data.split(':')
    tg_id = int(tg_id)

    if tg_id not in pending_teachers:
        await callback.message.edit_text('⚠️ Запрос не найден или уже обработан')
        return

    user_data = pending_teachers[tg_id]
    db.add_teacher(tg_id=user_data['tg_id'], name=user_data['username'])

    await callback.message.edit_text(
        text=f'✅ Преподаватель @{user_data["username"]} успешно добавлен',
        reply_markup=admin_panel()
    )

    await bot.send_message(
        chat_id=tg_id,
        text='🎉 Поздравляем! Ваша регистрация подтверждена.\n'
             'Теперь вы имеете доступ ко всем функциям системы.'
    )

    del pending_teachers[tg_id]


@dp.callback_query(F.data == 'exit')
async def return_to_admin_panel(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        '⚙️ Панель администратора',
        reply_markup=admin_panel()
    )


@dp.message(F.text == PASSWORD)
async def admin_access(message: types.Message):
    await message.answer(
        '⚙️ Панель администратора',
        reply_markup=admin_panel()
    )


@dp.callback_query(F.data == 'list_teachers')
async def show_teachers_list(call: types.CallbackQuery):
    teachers_list = db.get_all_teachers
    if not teachers_list:
        await call.message.edit_text(
            '📭 Список преподавателей пуст',
            reply_markup=admin_panel()
        )
        return

    await call.message.edit_text(
        '👨‍🏫 Список преподавателей',
        reply_markup=teachers(teachers_list)
    )


@dp.callback_query(F.data == 'new_teacher')
async def start_adding_teacher(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddTeacher.name)
    await callback.message.answer(
        "✏️ Введите ФИО преподавателя:"
    )


@dp.message(AddTeacher.name)
async def get_teacher_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        '🆔 Теперь введите Telegram ID преподавателя:'
    )
    await state.set_state(AddTeacher.tg_id)


@dp.message(AddTeacher.tg_id)
async def complete_teacher_add(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(
            '❌ Ошибка: ID должен содержать только цифры\n'
            'Пожалуйста, введите корректный Telegram ID:'
        )
        return

    await state.update_data(tg_id=int(message.text))
    data = await state.get_data()
    db.add_teacher(name=data['name'], tg_id=data['tg_id'])

    await message.answer(
        f'✅ Преподаватель {data["name"]} успешно добавлен',
        reply_markup=admin_panel()
    )
    await state.clear()


@dp.callback_query(F.data.startswith('teacher:'))
async def show_teacher_details(callback: types.CallbackQuery):
    teacher_id = int(callback.data.split(':')[1])
    teacher = db.get_teacher(tg_id=teacher_id)

    if not teacher:
        await callback.message.edit_text(
            '⚠️ Преподаватель не найден',
            reply_markup=admin_panel()
        )
        return

    groups_list = ', '.join([group.name for group in teacher.groups]) if teacher.groups else 'не назначены'
    notes = teacher.notes if teacher.notes else 'отсутствуют'

    await callback.message.edit_text(
        text=f'👨‍🏫 Профиль преподавателя:\n\n'
             f'📌 ФИО: {teacher.name}\n'
             f'👥 Группы: {groups_list}\n'
             f'📝 Замечания: {notes}\n'
             f'⭐ Баллы: {teacher.scores}',
        reply_markup=about(teacher)
    )

@dp.callback_query(F.data.startswith('edit_teacher_name:'))
async def start_edit_teacher_name(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split(':')
    await state.set_state(EditTeacher.name)
    await state.update_data(tg_id=int(data[-1]))
    await call.message.edit_text(
        '✏️ Введите новое имя для преподавателя:',
        reply_markup=main_menu()
    )

@dp.message(EditTeacher.name)
async def show_edit_teacher_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    try:
        data = await state.get_data()
        teacher = db.get_teacher(tg_id=int(data['tg_id']))
        groups_list = ', '.join([group.name for group in teacher.groups]) if teacher.groups else 'не назначены'
        notes = teacher.notes if teacher.notes else 'отсутствуют'
        db.edit_teacher_name(
            tg_id=int(data['tg_id']),
            new_name=data['name']
        )
        await message.answer(
            text=f'✅ Имя преподавателя успешно изменено!\n\n'
                 f'👨‍🏫 Профиль преподавателя:\n\n'
                 f'📌 ФИО: {teacher.name}\n'
                 f'👥 Группы: {groups_list}\n'
                 f'📝 Замечания: {notes}\n'
                 f'⭐ Баллы: {teacher.scores}',
            reply_markup=about(teacher)  # Предполагается, что teacher доступен
        )
        await state.clear()
    except Exception as e:
        print(f"Ошибка при изменении имени преподавателя: {e}")
        await message.answer(
            '❌ Произошла ошибка при изменении имени. Пожалуйста, попробуйте позже.',
            reply_markup=main_menu()
        )
        await state.clear()

@dp.callback_query(F.data.startswith('statistic:'))
async def show_statistics(call: types.CallbackQuery, state: FSMContext):
    teacher = db.get_teacher(tg_id=int(call.data.split(':')[1]))
    if teacher:
        teacher_scores_percent = teacher.max_score // 100
        stat_list = db.get_teacher_statistic(tg_id=teacher.tg_id)
        if len(stat_list) > 0:
            for stat in stat_list:
                await call.message.answer(f'Учитель {stat.teacher_name}\n'
                                          f'Месяц: {stat.month}\n'
                                          f'Баллы: {stat.score} ({stat.score // teacher_scores_percent}%)\n',
                                          )
            await call.message.answer("Что дальше?", reply_markup=about(teacher))
        else:
            await call.message.edit_text(f'Статистика на этого преподавателя еще не готова', reply_markup=main_menu())

@dp.callback_query(F.data.startswith('delete:'))
async def delete_teacher(call: types.CallbackQuery):
    teacher_id = int(call.data.split(':')[1])
    db.delete_teacher(tg_id=teacher_id)

    await call.message.edit_text(
        '🗑️ Преподаватель успешно удалён',
        reply_markup=admin_panel()
    )


@dp.callback_query(F.data.startswith('mistake:'))
async def report_mistake(call: types.CallbackQuery, state: FSMContext):
    teacher_id = int(call.data.split(':')[1])
    await state.set_state(Misstake.problem)
    await state.update_data(tg_id=teacher_id)

    await call.message.edit_text(
        '📝 Опишите проблему/замечание:',
        reply_markup=main_menu()
    )


@dp.message(Misstake.problem)
async def get_mistake_description(msg: types.Message, state: FSMContext):
    await state.update_data(problem=msg.text)
    await state.set_state(Misstake.group_name)
    data = await state.get_data()

    groups_list = db.get_teachers_group(data['tg_id'])
    if groups_list:
        await msg.answer(
            '👥 Выберите группу, в которой возникла проблема:',
            reply_markup=groups(groups_list)
        )
    else:
        await state.set_state(Misstake.scores)
        await msg.answer(
            '🔢 Укажите количество баллов для вычета:',
            reply_markup=main_menu()
        )


@dp.callback_query(Misstake.group_name)
async def select_group_for_mistake(call: types.CallbackQuery, state: FSMContext):
    group_id = int(call.data.split(':')[1])
    group = db.get_one_group(group_id)
    await state.update_data(group=group)
    await state.set_state(Misstake.scores)

    await call.message.answer(
        '🔢 Укажите количество баллов для вычета:',
        reply_markup=main_menu()
    )


@dp.message(Misstake.scores)
async def process_score_deduction(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer(
            '❌ Ошибка: введите числовое значение',
            reply_markup=main_menu()
        )
        return

    await state.update_data(scores=int(msg.text))
    data = await state.get_data()

    group_info = f"В группе: {str(data['group'].name)}, " if data.get('group') else ""
    problem_text = f"{group_info}{str(data['problem']).lower()}"

    db.subtract_score(
        tg_id=data['tg_id'],
        value=data['scores'],
        note=problem_text
    )

    await msg.answer(
        '✅ Замечание успешно зарегистрировано',
        reply_markup=admin_panel()
    )

    try:
        await bot.send_message(
            chat_id=data['tg_id'],
            text=f'📢 Уведомление:\n\n'
                 f'❗ Зафиксировано замечание: {problem_text}\n'
                 f'➖ Снято баллов: {data["scores"]}\n\n'
                 f'ℹ️ Пожалуйста, примите меры для устранения.'
        )
    except Exception as e:
        print(f"Ошибка отправки уведомления: {e}")
        await msg.answer(
            '⚠️ Не удалось отправить уведомление преподавателю',
            reply_markup=admin_panel()
        )

    await state.clear()


@dp.callback_query(F.data.startswith('new_group:'))
async def start_adding_group(call: types.CallbackQuery, state: FSMContext):
    teacher_id = int(call.data.split(':')[1])
    await state.set_state(AddGroup.group_name)
    await state.update_data(tg_id=teacher_id)

    await call.message.answer(
        '✏️ Введите название новой группы:',
        reply_markup=main_menu()
    )

@dp.message(AddGroup.group_name)
async def complete_group_add(message: types.Message, state: FSMContext):
    await state.update_data(group_name=message.text)
    await message.answer('Введите количество баллов за группу', reply_markup=main_menu())
    await state.set_state(AddGroup.scores)

@dp.message(AddGroup.scores)
async def score_adding_group(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(scores=int(message.text))
        data = await state.get_data()
        db.create_group(
            group_name=data['group_name'],
            teacher_tg_id=data['tg_id'],
            scores=data['scores'],
        )

        await message.answer(
            f'✅ Группа "{data["group_name"]}" успешно создана',
            reply_markup=admin_panel()
        )
        await state.clear()
    else:
        await message.answer('Введите количество баллов в числовом формате', reply_markup=main_menu())





@dp.callback_query(F.data.startswith('delete_group:'))
async def show_list_groups_to_delete(call: types.CallbackQuery, state: FSMContext):
    teacher_id = call.data.split(':')[1]
    groups_list = db.get_teachers_group(tg_id=int(teacher_id))
    await call.message.edit_text('🗑️ Выберите группу для удаления', reply_markup=groups(groups_list=groups_list))

@dp.callback_query(F.data.startswith('group:'))
async def delete_group(call: types.CallbackQuery, state: FSMContext):
    group_id = int(call.data.split(':')[1])
    db.delete_group(group_id)
    await call.message.edit_text('✅ Группа успешно удалена', reply_markup=main_menu())