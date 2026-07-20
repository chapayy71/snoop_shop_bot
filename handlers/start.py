from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.menu import age_keyboard, main_menu

from database.session import async_session
from database.models import User

from sqlalchemy import select


router = Router()


@router.message(Command("start"))
async def start(message: Message):

    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.telegram_id == message.from_user.id
            )
        )

        user = result.scalar()


        if user and user.age_verified:

            await message.answer(
                "С возвращением! 👋",
                reply_markup=main_menu
            )

        else:

            await message.answer(
                "Здравствуйте!\n\n"
                "Для входа подтвердите, что вам есть 18 лет.",
                reply_markup=age_keyboard
            )


@router.message(
    lambda message:
    message.text == "🔞 Мне есть 18 лет"
)
async def age_confirm(message: Message):

    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.telegram_id == message.from_user.id
            )
        )

        user = result.scalar()


        if not user:

            user = User(
                telegram_id=message.from_user.id,
                age_verified=True
            )

            session.add(user)

        else:

            user.age_verified = True


        await session.commit()


    await message.answer(
        "Возраст подтвержден ✅\n\n"
        "Добро пожаловать в магазин!",
        reply_markup=main_menu
    )