from aiogram.filters import Filter
from aiogram import types
from data import DataBase
from data.db import OWNER_ID

db = DataBase()

class IsAdminMessage(Filter):
    async def __call__(self, message: types.Message):
        teacher = db.get_teacher(message.from_user.id)
        return teacher.is_admin

class IsAdminCall(Filter):
    async def __call__(self, call: types.CallbackQuery):
        teacher = db.get_teacher(call.from_user.id)
        return teacher.is_admin

class IsOwnerMessage(Filter):
    async def __call__(self, message: types.Message):
        return int(message.from_user.id) == int(OWNER_ID)

class IsOwnerCall(Filter):
    async def __call__(self, call: types.CallbackQuery):
        return int(call.from_user.id) == int(OWNER_ID)