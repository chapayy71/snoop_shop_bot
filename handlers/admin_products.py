from database.models import Order, OrderItem, Product, User
from database.session import async_session
from sqlalchemy import select
from states.product import ProductEdit
from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from sqlalchemy import delete
from aiogram.fsm.context import FSMContext
from states.product import ProductAdd
from config import ADMIN_ID
from aiogram.fsm.context import FSMContext
from keyboards.admin_products import products_delete_keyboard
from states.product import ProductAdd, ProductDelete
from aiogram.types import CallbackQuery
from keyboards.admin_products import product_list_keyboard, edit_keyboard
from keyboards.admin_products import edit_keyboard, product_list_keyboard
from database.session import async_session
from database.models import Category, Product

from sqlalchemy import select

router = Router()


admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="➕ Добавить товар"
            )
        ],
        [
            KeyboardButton(
                text="✏️ Изменить товар"
            )
        ],
        [
            KeyboardButton(
                text="🗑 Удалить товар"
            )
        ],
        [
            KeyboardButton(
                text="📦 Заказы"
            )
        ]
    ],
    resize_keyboard=True
)

@router.message(Command("admin"))
async def admin_panel(
    message: Message
):

    if message.from_user.id != ADMIN_ID:
        await message.answer(
            "❌ Нет доступа."
        )
        return


    await message.answer(
        "👑 Админ панель",
        reply_markup=admin_keyboard
    )
@router.message(
    lambda message:
    message.text == "➕ Добавить товар"
)
async def add_product_start(
    message: Message,
    state: FSMContext
):

    if message.from_user.id != ADMIN_ID:
        return

    await state.clear()


    await message.answer(
        "📂 Введите ID категории:"
    )

    await state.set_state(
        ProductAdd.category
    )
@router.message(ProductAdd.category)
async def product_category(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        category_id=int(message.text)
    )

    await message.answer(
        "✏️ Введите название товара:"
    )

    await state.set_state(
        ProductAdd.name
    )
@router.message(ProductAdd.name)
async def product_name(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        name=message.text
    )

    await message.answer(
        "📝 Введите описание товара:"
    )

    await state.set_state(
        ProductAdd.description
    )


@router.message(ProductAdd.description)
async def product_description(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        description=message.text
    )

    await message.answer(
        "💰 Введите цену товара:"
    )

    await state.set_state(
        ProductAdd.price
    )


@router.message(ProductAdd.price)
async def product_price(
    message: Message,
    state: FSMContext
):

    try:
        price = int(message.text)
    except ValueError:
        await message.answer(
            "❌ Введите число."
        )
        return


    await state.update_data(
        price=price
    )

    await message.answer(
        "📦 Введите количество на складе:"
    )

    await state.set_state(
        ProductAdd.stock
    )


@router.message(ProductAdd.stock)
async def product_stock(
    message: Message,
    state: FSMContext
):

    try:
        stock = int(message.text)
    except ValueError:
        await message.answer(
            "❌ Введите число."
        )
        return


    await state.update_data(
        stock=stock
    )


    data = await state.get_data()


    async with async_session() as session:

        product = Product(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            stock=data["stock"],
            category_id=data["category_id"]
        )

        session.add(product)

        await session.commit()


    await message.answer(
        f"✅ Товар добавлен!\n\n"
        f"📦 {data['name']}\n"
        f"💰 Цена: {data['price']} ₽\n"
        f"Количество: {data['stock']} шт."
    )

@router.message(
    lambda message:
    message.text == "🗑 Удалить товар"
)
async def delete_product_start(
    message: Message
):

    if message.from_user.id != ADMIN_ID:
        return


    async with async_session() as session:

        result = await session.execute(
            select(Product)
        )

        products = result.scalars().all()


    if not products:
        await message.answer(
            "Товаров нет."
        )
        return


    await message.answer(
        "Выберите товар для удаления:",
        reply_markup=products_delete_keyboard(products)
    )
@router.callback_query(
    lambda c: c.data.startswith("delete_product_")
)
async def delete_product_callback(
    callback: CallbackQuery
):

    product_id = int(
        callback.data.split("_")[-1]
    )


    async with async_session() as session:

        product = await session.get(
            Product,
            product_id
        )


        if product:
            await session.delete(product)
            await session.commit()


    await callback.message.answer(
        "✅ Товар удален."
    )
@router.message(
    lambda message:
    message.text == "✏️ Изменить товар"
)
async def edit_product_start(
    message: Message,
    state: FSMContext
):

    if message.from_user.id != ADMIN_ID:
        return

    await state.clear()


    async with async_session() as session:

        result = await session.execute(
            select(Product)
        )

        products = result.scalars().all()


    if not products:
        await message.answer(
            "Товаров нет."
        )
        return


    await message.answer(
        "Выберите товар:",
        reply_markup=product_list_keyboard(
            products,
            "edit_product"
        )
    )
@router.callback_query(
    lambda c: c.data.startswith("edit_product_")
)
async def edit_product_menu(
    callback: CallbackQuery
):

    product_id = int(
        callback.data.split("_")[-1]
    )


    await callback.message.answer(
        "Что изменить?",
        reply_markup=edit_keyboard(product_id)
    )
@router.callback_query(
    lambda c: c.data.startswith("edit_price_")
)
async def edit_price_start(
    callback: CallbackQuery,
    state: FSMContext
):

    product_id = int(
        callback.data.split("_")[-1]
    )

    await state.update_data(
        product_id=product_id
    )

    await callback.message.answer(
        "Введите новую цену:"
    )

    await state.set_state(
        ProductEdit.price
    )

    await callback.answer()

@router.message(ProductEdit.price)
async def edit_price(
    message: Message,
    state: FSMContext
):

    try:
        price = int(message.text)

    except ValueError:
        await message.answer(
            "Введите число."
        )
        return


    data = await state.get_data()


    async with async_session() as session:

        product = await session.get(
            Product,
            data["product_id"]
        )

        if product:
            product.price = price

            await session.commit()


    await message.answer(
        "✅ Цена изменена."
    )

@router.callback_query(
    lambda c: c.data.startswith("edit_stock_")
)
async def edit_stock_start(
    callback: CallbackQuery,
    state: FSMContext
):
  
    print("КНОПКА ОСТАТКА НАЖАТА")

    product_id = int(
        callback.data.split("_")[-1]
    )

    await state.update_data(
        product_id=product_id
    )

    await callback.message.answer(
        "Введите новое количество:"
    )

    await state.set_state(
        ProductEdit.stock
    )

    await callback.answer()

@router.message(ProductEdit.stock)
async def edit_stock(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    print("Данные изменения:", data)


    try:
        stock = int(message.text)

    except ValueError:

        await message.answer(
            "Введите только число."
        )

        return


    async with async_session() as session:

        product = await session.get(
            Product,
            data["product_id"]
        )


        if not product:

            await message.answer(
                "Товар не найден."
            )

            await state.clear()
            return


        product.stock = stock

        await session.commit()


    await message.answer(
        f"✅ Остаток изменён: {stock}"
    )

@router.message(
    lambda message:
    message.text == "📦 Заказы"
)
async def admin_orders(
    message: Message,
    state: FSMContext
):

    await state.clear()

    if message.from_user.id != int(ADMIN_ID):
        return


    async with async_session() as session:

        result = await session.execute(
            select(Order)
            .order_by(Order.id.desc())
        )

        orders = result.scalars().all()


    if not orders:

        await message.answer(
            "📦 Заказов пока нет."
        )

        return


    for order in orders:


        async with async_session() as session:

            items_result = await session.execute(
                select(OrderItem, Product)
                .join(
                    Product,
                    OrderItem.product_id == Product.id
                )
                .where(
                    OrderItem.order_id == order.id
                )
            )

            items = items_result.all()


        products_text = ""

        for item, product in items:

            products_text += (
                f"• {product.name} "
                f"x{item.quantity}\n"
            )


        await message.answer(
            f"📦 Заказ #{order.id}\n\n"
            f"👤 {order.customer_name}\n"
            f"💬 Telegram: {order.telegram_username or 'Нет username'}\n"
            f"📱 {order.phone}\n"
            f"🏠 {order.address}\n\n"
            f"🛒 Товары:\n"
            f"{products_text}\n"
            f"💰 {order.total_price} ₽\n"
            f"📌 {order.status}"
        )

    await state.clear()