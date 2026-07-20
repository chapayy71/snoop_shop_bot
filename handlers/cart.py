from aiogram import Router
from aiogram.types import Message, CallbackQuery
from keyboards.cart import cart_keyboard
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
        reply_markup=cart_keyboard(items)
    )
@router.callback_query(
    lambda c: c.data.startswith("delete_cart_")
)
async def delete_cart_item(
    callback: CallbackQuery
):

    item_id = int(
        callback.data.split("_")[2]
    )


    async with async_session() as session:

        result = await session.execute(
            select(CartItem).where(
                CartItem.id == item_id
            )
        )

        item = result.scalar()


        if item:

            await session.delete(item)

            await session.commit()


    await callback.answer(
        "✅ Товар удалён"
    )


    await callback.message.edit_text(
        "🛒 Товар удалён из корзины."
    )
@router.callback_query(
    lambda c: c.data.startswith("cart_plus_")
)
async def cart_plus(
    callback: CallbackQuery
):

    item_id = int(
        callback.data.split("_")[2]
    )


    async with async_session() as session:

        result = await session.execute(
            select(CartItem).where(
                CartItem.id == item_id
            )
        )

        item = result.scalar()

        if item:
            item.quantity += 1
            await session.commit()


    await callback.answer("Количество увеличено")
    await callback.message.delete()

@router.callback_query(
    lambda c: c.data.startswith("cart_minus_")
)
async def cart_minus(
    callback: CallbackQuery
):

    item_id = int(
        callback.data.split("_")[2]
    )


    async with async_session() as session:

        result = await session.execute(
            select(CartItem).where(
                CartItem.id == item_id
            )
        )

        item = result.scalar()


        if item:

            if item.quantity > 1:
                item.quantity -= 1

            else:
                await session.delete(item)


            await session.commit()


    await callback.answer("Количество изменено")
    await callback.message.delete()