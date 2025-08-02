from loader import dp
from permissions import IsAdminCall, IsAdminMessage

from aiogram import types, html, F

from keyboards.admin.inline import admin_panel, nicho

@dp.message(F.text == '308012')
async def start(message: types.Message):
    return await message.answer('Админ панель', reply_markup=admin_panel())

@dp.callback_query(F.data == '/panel')
async def panel(call: types.CallbackQuery):
    return await call.message.edit_text(text='Чо хотел', inline_message_id=call.inline_message_id, reply_markup=nicho())

@dp.callback_query(F.data == '/nicho')
async def poh(call: types.CallbackQuery):
    return await call.message.edit_text(text='Даунище', inline_message_id=call.inline_message_id, reply_markup=admin_panel())