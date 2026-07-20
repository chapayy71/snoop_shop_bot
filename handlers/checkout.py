from aiogram import Router, Bot
from config import ADMIN_ID
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from database.models import (
    User,
    CartItem,
    Product,
    Order,
    OrderItem
)

from database.session import async_session
from sqlalchemy import select
from states.checkout import Checkout

router = Router()


@router.callback_query(lambda c: c.data == "checkout")
async def checkout_start(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.message.answer(
        "👤 Введите ваше имя:"
    )

    await state.set_state(
        Checkout.name
    )

    await callback.answer()


@router.message(Checkout.name)
async def checkout_name(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        name=message.text
    )

    await message.answer(
        "📱 Введите ваш телефон:"
    )

    await state.set_state(
        Checkout.phone
    )


@router.message(Checkout.phone)
async def checkout_phone(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        phone=message.text
    )

    await message.answer(
        "🏠 Введите адрес доставки:"
    )

    await state.set_state(
        Checkout.address
    )

@router.message(Checkout.address)
async def checkout_address(
    message: Message,
    state: FSMContext,
    bot: Bot
):

    data = await state.get_data()

    async with async_session() as session:

        user_result = await session.execute(
            select(User).where(
                User.telegram_id == message.from_user.id
            )
        )

        user = user_result.scalar()

        if not user:
            await message.answer(
                "❌ Пользователь не найден."
            )
            await state.clear()
            return


        cart_result = await session.execute(
            select(CartItem, Product)
            .join(
                Product,
                CartItem.product_id == Product.id
            )
            .where(
                CartItem.user_id == user.id
            )
        )

        cart_items = cart_result.all()

        if not cart_items:
            await message.answer(
                "🛒 Корзина пустая."
            )
            await state.clear()
            return


        total = 0

        for item, product in cart_items:
            total += product.price * item.quantity


        order = Order(
            user_id=user.id,
            customer_name=data["name"],
            phone=data["phone"],
            address=message.text,
            total_price=total
        )

        session.add(order)

        await session.flush()


        for item, product in cart_items:

            product.stock -= item.quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            )

            session.add(order_item)


        for item, product in cart_items:
            await session.delete(item)


        await session.commit()


        await message.answer(
        f"✅ Заказ оформлен!\n\n"
        f"Номер заказа: #{order.id}\n"
        f"Сумма: {total} ₽"
    )


    username = message.from_user.username

    if username:
        username_text = f"@{username}"
    else:
        username_text = "Нет username"


    products_text = ""

    for item, product in cart_items:
        products_text += (
            f"• {product.name}\n"
            f"  Количество: {item.quantity} шт.\n"
            f"  Цена: {product.price} ₽\n\n"
        )


    await bot.send_message(
        ADMIN_ID,
        f"🆕 Новый заказ!\n\n"
        f"№{order.id}\n\n"
        f"👤 Клиент: {data['name']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"💬 Telegram: {username_text}\n"
        f"🏠 Адрес: {message.text}\n\n"
        f"📦 Товары:\n"
        f"{products_text}"
        f"💰 Итого: {total} ₽"
    )


    await state.clear()