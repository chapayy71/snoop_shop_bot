from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cart_keyboard(items):

    buttons = []

    for item, product in items:

        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"❌ {product.name}",
                    callback_data=f"delete_cart_{item.id}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="✅ Оформить заказ",
                callback_data="checkout"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )