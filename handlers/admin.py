from aiogram.fsm.context import FSMContext

from data import DataBase, owner

from loader import dp, bot
from permissions import IsAdminCall, IsAdminMessage

from states import AddGroup, AddTeacher, Misstake

from aiogram import types, F

from keyboards.admin.inline import *

db = DataBase()

pending_teachers = dict()

@dp.message(F.text == '/start')
async def _id(message: types.Message, state: FSMContext):
    teacher = db.get_teacher(message.from_user.id)
    if not teacher:
        pending_teachers[message.from_user.id] = {
            'tg_id': message.from_user.id,
            'username': message.from_user.username,
        }
        await message.answer(f'Я отправил заявку администратору на вашу регистрацию в качестве преподавателя')
        await bot.send_message(chat_id=owner, text=f'Пользователь @{message.from_user.username} отправил запрос на регистрацию, регистрируем?',
                               reply_markup=teacher_registration(tg_id=message.from_user.id,
                                                                 username=message.from_user.username))
    else:
        await message.answer('Ты уже зарегистрирован')

@dp.callback_query(F.data.startswith('registration'))
async def registration(callback_data: types.CallbackQuery, state: FSMContext):
    _, tg_id, username = callback_data.data.split(':')
    tg_id = int(tg_id)
    if tg_id not in pending_teachers:
        await callback_data.message.edit_text('Запрос не найден или уже обработан')
        return
    user_data = pending_teachers[tg_id]
    db.add_teacher(tg_id=user_data['tg_id'], name=user_data['username'])
    await callback_data.message.edit_text(text=f'Учитель @{user_data['username']} добавлен в общий список',
                                          reply_markup=main_menu())
    await bot.send_message(text='Твоя регистрация завершена', chat_id=tg_id)
    del pending_teachers[tg_id]



@dp.callback_query(F.data == 'exit')
async def start_at_call(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    return await call.message.edit_text('Админ панель', reply_markup=admin_panel())

@dp.message(F.text == '308012')
async def start(message: types.Message, state: FSMContext):
    return await message.answer('Админ панель', reply_markup=admin_panel())

@dp.callback_query(F.data == 'list_teachers')
async def list_teachers(call: types.CallbackQuery, state: FSMContext):
    return await call.message.edit_text('Список учителей', inline_message_id=call.inline_message_id, reply_markup=teachers(
        db.get_all_teachers))

@dp.callback_query(F.data == 'new_teacher')
async def new_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddTeacher.name)
    await callback_query.message.answer("Введите имя учителя")

@dp.message(AddTeacher.name)
async def add_teacher(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Теперь введите его телеграмм id')
    await state.set_state(AddTeacher.tg_id)

@dp.message(AddTeacher.tg_id)
async def add_teacher(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Введите его айди в цифровом виде')
        return
    await state.update_data(tg_id=int(message.text))
    data = await state.get_data()
    db.add_teacher(name=data['name'], tg_id=data['tg_id'])
    await message.answer('Учитель добавлен в общий список', reply_markup=main_menu())
    await state.clear()

@dp.callback_query(F.data.startswith('teacher:'))
async def teacher_about(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split(':')[1]
    teacher = db.get_teacher(tg_id=int(data))
    if teacher is not None:
        group_names = ', '.join([group.name for group in teacher.groups]) if teacher.groups else 'их нет'
        await callback_query.message.edit_text(text=f'''
Учитель: {teacher.name}
Его группы: {group_names}
Косяки: {teacher.notes if teacher.notes else "их нет"}
Баллы: {teacher.scores}
''',
                                               inline_message_id=callback_query.inline_message_id,
                                               reply_markup=about(teacher))
    else:
        await callback_query.message.edit_text('Чето хуйня какая то', inline_message_id=callback_query.inline_message_id)

@dp.callback_query(F.data.startswith('delete:') | F.data.startswith('misstake:'))
async def put_or_delete(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split(':')
    if data[0] == 'misstake':
        await state.set_state(Misstake.problem)
        await state.update_data(tg_id=int(data[1]))
        await call.message.edit_text('Какой косяк че не так сделал', reply_markup=main_menu())
    elif data[0] == 'delete':
        db.delete_teacher(tg_id=int(data[1]))
        await call.message.edit_text('Удалил учителя из общего списка', reply_markup=main_menu())

@dp.message(Misstake.problem)
async def _misstake(msg: types.Message, state: FSMContext):
    await state.update_data(problem=msg.text)
    await state.set_state(Misstake.scores)
    await msg.answer('Сколько баллов снимаем')

@dp.message(Misstake.scores)
async def substract(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer('Введи число')
    await state.update_data(scores=msg.text)
    data = await state.get_data()
    db.subtract_score(tg_id=int(data['tg_id']), value=int(data['scores']), note=data['problem'])
    await msg.answer('Косяк записан', reply_markup=main_menu())
    try:
        await bot.send_message(chat_id=data['tg_id'], text=f'{data['problem']}, сняли с тебя {data["scores"]} баллов')
    except Exception as e:
        print(e)
        await msg.answer('Учитель не зарегистрирован в боте так что я не смог отправить ему уведомление')
    await state.clear()



@dp.callback_query(F.data.startswith('new_group:'))
async def new_group(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split(':')
    await state.set_state(AddGroup.group_name)
    await state.update_data(tg_id=int(data[-1]))
    await call.message.answer(text='Введите название группы', reply_markup=main_menu())

@dp.message(AddGroup.group_name)
async def add_group(message: types.Message, state: FSMContext):
    await state.update_data(group_name=message.text)
    data = await state.get_data()
    db.create_group(group_name=data['group_name'], teacher_tg_id=data['tg_id'])
    await message.answer(text='Добавлена группа', reply_markup=main_menu())
    await state.clear()

