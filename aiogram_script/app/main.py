from aiogram import Bot, Dispatcher
from views.master_router import master_router 
from middleware.auth import AuthMiddleware
import asyncio
import os


async def main():
    bot = Bot(token = os.getenv("BOT_TOKEN"))

    dp = Dispatcher()
    
    dp.message.outer_middleware(AuthMiddleware())
    dp.callback_query.outer_middleware(AuthMiddleware())

    dp.include_router(master_router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())