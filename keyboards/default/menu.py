from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def button_generator_kod_access():
    btn = KeyboardButton('создать код чата 🆔')
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(btn)
    return markup
