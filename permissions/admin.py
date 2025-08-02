from aiogram.filters import Filter
from aiogram import types
from data.db import db

class IsAdmin(Filter):
    async def __call__(self, message: types.Message, tg_id: int):
        is_admin = db.is_admin(message.from_user.id)
        return is_admin
