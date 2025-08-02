from loader import dp
from permissions import IsAdmin

from aiogram import types, html, F

@dp.message_handler(F.text == '/admin', IsAdmin())
async def start(message: types.Message):
    return await message.answer('Админ панель')