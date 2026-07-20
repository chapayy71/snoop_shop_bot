import asyncio

from aiogram import Bot, Dispatcher, Router

from config import BOT_TOKEN
from handlers.admin_products import router as admin_products_router
from handlers.start import router as start_router
from handlers.catalog import router as catalog_router
from handlers.cart import router as cart_router
from handlers.checkout import router as checkout_router
from database.session import engine

from database.models import Base


async def create_db():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )


async def main():

    await create_db()

    bot = Bot(
        token=BOT_TOKEN
    )

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(catalog_router)
    dp.include_router(cart_router)
    dp.include_router(checkout_router)
    dp.include_router(admin_products_router)

    print("Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())