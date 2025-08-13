import datetime

from data import DataBase

from handlers import dp
import asyncio
import sys
import logging
from loader import bot


async def monthly_reset():
    db = DataBase()
    now = datetime.datetime.now()

    if now.day == 1:
        db.reset_monthly_scores()

    while True:
        now = datetime.datetime.now()
        if now.day == 1:
            db.reset_monthly_scores()
            await asyncio.sleep(172800)  # 48 часов
        else:
            # Проверяем ежедневно (в полночь)
            tomorrow = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0)
            seconds_until_midnight = (tomorrow - now).total_seconds()
            await asyncio.sleep(seconds_until_midnight)


async def start():
    DataBase.create_table()
    asyncio.create_task(monthly_reset())  # Запускаем фоновую задачу
    await bot.delete_webhook()
    print('Бот запущен')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start())


