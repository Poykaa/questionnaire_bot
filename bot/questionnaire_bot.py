from aiogram.utils import executor
from loader import dp
from database import initial_db
from handlers import dp


async def on_start(_):
    print('Bot is online!')
    initial_db()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_start)
