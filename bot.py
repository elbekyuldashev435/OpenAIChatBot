import asyncio
from aiogram import Bot, Dispatcher
from conf import BOT_TOKEN
from database import init_db
from handlers import router


async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("✅ Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
