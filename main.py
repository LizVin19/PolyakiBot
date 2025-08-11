from database.bd import init_users_db, init_cities_db
from loader import bot
import logging
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands


logging.basicConfig(level=logging.INFO)
init_users_db()
init_cities_db()

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    logging.info('Bot started')
    bot.infinity_polling()
