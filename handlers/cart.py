from aiogram import Router
from aiogram.types import Message
from keyboards.cart import checkout_keyboard
from database.session import async_session
from database.models import CartItem, Product, User

from sqlalchemy import select


router = Router()


@router.message(
    lambda message:
    message.text == "🛒 Корзина"
)
async def cart(message: Message):

    async with async_session() as session:

        user_result = await session.execute(
            select(User).where(
                User.telegram_id == message.from_user.id
            )
        )

        user = user_result.scalar()


        if not user:
            await message.answer(
                "Пользователь не найден."
            )
            return


        result = await session.execute(
            select(CartItem, Product)
            .join(
                Product,
                CartItem.product_id == Product.id
            )
            .where(
                CartItem.user_id == user.id
            )
        )


        items = result.all()


    if not items:

        await message.answer(
            "🛒 Корзина пуста."
        )
        return


    text = "🛒 Ваша корзина:\n\n"

    total = 0


    for item, product in items:

        summa = product.price * item.quantity

        total += summa

        text += (
            f"📦 {product.name}\n"
            f"Количество: {item.quantity}\n"
            f"Цена: {summa} ₽\n\n"
        )


    text += (
        f"💰 Итого: {total} ₽"
    )


    await message.answer(
        text,
        reply_markup=checkout_keyboard
    )