from aiogram.fsm.context import FSMContext

from data import DataBase

from loader import dp
from permissions import IsAdminCall, IsAdminMessage

from states import AddGroup, AddTeacher

from aiogram import types, F

from keyboards.admin.inline import admin_panel, nicho, teachers

db = DataBase()

@dp.message(F.text == '/id')
async def _id(message: types.Message):
    return await message.answer(f'Ваш id: {message.from_user.id}')

@dp.callback_query(F.data == 'exit')
async def start_at_call(call: types.CallbackQuery, state: FSMContext):
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
    await message.answer('Учитель добавлен в общий список')
    await state.clear()