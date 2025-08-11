from telebot.types import Message
from loader import bot
import logging


@bot.message_handler(commands=['start'])
def bot_start(m: Message):
    logging.info(f'user {m.from_user.username} connected')
    bot.reply_to(m, f'Hola {m.from_user.full_name}')