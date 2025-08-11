import logging
from telebot.types import Message
from loader import bot
from config import DEFAULT_COMMANDS

def_commands = [f'/{cmd}' for cmd, _ in DEFAULT_COMMANDS]


@bot.message_handler(
    func=lambda m: (
            # not m.text.startswith('/')
            m.text not in def_commands
            and bot.get_state(chat_id=m.chat.id, user_id=m.from_user.id) is None
    )
)
def bot_echo(m: Message):
    logging.info(f'user {m.from_user.username} dumped into echo')
    bot.reply_to(m, f'echo')