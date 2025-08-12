
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from data import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

