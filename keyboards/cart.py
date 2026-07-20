from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

checkout_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🛒 Оформить заказ",
                callback_data="checkout"
            )
        ]
    ]
)