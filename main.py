from data import DataBase

from handlers import dp
import asyncio
import sys
import logging
from loader import bot

async def start():
    DataBase.create_table()
    await bot.delete_webhook()
    print('Бот запущен')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start())


