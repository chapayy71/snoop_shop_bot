from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database.session import async_session
from database.models import Product

from sqlalchemy import select


router = Router()


@router.message(
    lambda message:
    message.text == "🛍 Каталог"
)
async def catalog(message: Message):

    async with async_session() as session:

        result = await session.execute(
            select(Product)
        )

        products = result.scalars().all()


    if not products:
        await message.answer(
            "Каталог пока пуст."
        )
        return


    for product in products:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Добавить в корзину",
                        callback_data=f"add_{product.id}"
                    )
                ]
            ]
        )


        await message.answer(
            f"📦 {product.name}\n\n"
            f"{product.description}\n\n"
            f"💰 Цена: {product.price} ₽\n"
            f"Осталось: {product.stock} шт.",
            reply_markup=keyboard
        )

from aiogram.types import CallbackQuery

from database.models import CartItem, User
from sqlalchemy import select


@router.callback_query(
    lambda call: call.data.startswith("add_")
)
async def add_to_cart(call: CallbackQuery):

    product_id = int(
        call.data.split("_")[1]
    )


    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.telegram_id == call.from_user.id
            )
        )

        user = result.scalar()


        if not user:
            await call.answer(
                "Сначала подтвердите возраст"
            )
            return


        item = CartItem(
            user_id=user.id,
            product_id=product_id,
            quantity=1
        )

        session.add(item)

        await session.commit()


    await call.answer(
        "Добавлено в корзину ✅"
    )