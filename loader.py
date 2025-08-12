
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from data import token

bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())

