from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


age_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="🔞 Мне есть 18 лет"
            )
        ]
    ],
    resize_keyboard=True
)


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛍 Каталог"),
            KeyboardButton(text="🛒 Корзина")
        ],
        [
            KeyboardButton(text="📦 Мои заказы"),
            KeyboardButton(text="💬 Поддержка")
        ]
    ],
    resize_keyboard=True
)