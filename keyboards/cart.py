from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cart_keyboard(items):

    buttons = []


    for item, product in items:

        buttons.append(
            [
                InlineKeyboardButton(
                    text="➖",
                    callback_data=f"cart_minus_{item.id}"
                ),
                InlineKeyboardButton(
                    text=f"{item.quantity}",
                    callback_data="none"
                ),
                InlineKeyboardButton(
                    text="➕",
                    callback_data=f"cart_plus_{item.id}"
                )
            ]
        )


        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"❌ Удалить {product.name}",
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