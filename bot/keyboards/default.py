from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Katalog')
        ],
        [
            KeyboardButton(text='Karzinka')
        ],
        [
            KeyboardButton(text='Bot Haqida!')
        ]
    ], resize_keyboard=True
)
