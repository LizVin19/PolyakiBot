from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_city_keyboard(city_list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    for city in city_list:
        keyboard.add(InlineKeyboardButton(text=city, callback_data=f'city_{city}'))
    return keyboard