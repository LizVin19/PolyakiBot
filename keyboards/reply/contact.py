from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def request_contact() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(
        KeyboardButton(text='send', request_contact=True),
        KeyboardButton(text='no')
    )
    return keyboard