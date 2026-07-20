from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def products_delete_keyboard(products):

    buttons = []

    for product in products:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"🗑 {product.name} | {product.price} ₽",
                    callback_data=f"delete_product_{product.id}"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def product_list_keyboard(products, action):

    buttons = []

    for product in products:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{product.name} | {product.price} ₽",
                    callback_data=f"{action}_{product.id}"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def edit_keyboard(product_id):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💰 Цена",
                    callback_data=f"edit_price_{product_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📦 Остаток",
                    callback_data=f"edit_stock_{product_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📝 Описание",
                    callback_data=f"edit_desc_{product_id}"
                )
            ]
        ]
    )