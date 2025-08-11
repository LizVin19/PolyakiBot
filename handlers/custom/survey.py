from loader import bot
from states.contact_info import UserInfoState
from telebot.types import Message, CallbackQuery
import pycountry
import logging
from database.bd import get_cities_by_country
from keyboards.inline.city_loc import generate_city_keyboard
from keyboards.reply.contact import request_contact
from load_cities import load_cities_for_country


@bot.message_handler(commands=['survey'])
def survey(m: Message) -> None:
    bot.set_state(user_id=m.from_user.id, state=UserInfoState.name, chat_id=m.chat.id)
    bot.send_message(chat_id=m.chat.id,
                     text=f'Hi, {m.from_user.username}! What is your name?')


@bot.message_handler(state=UserInfoState.name)
def get_name(m: Message) -> None:
    logging.info(f'[get_name] user={m.from_user.username}, text={m.text}')

    if m.text.isalpha():

        with bot.retrieve_data(user_id=m.from_user.id, chat_id=m.chat.id) as data:
            data['name'] = m.text

            logging.info(f'[get_name] Saved name: {m.text}')

        bot.send_message(chat_id=m.chat.id, text='Now enter your age')
        bot.set_state(user_id=m.from_user.id, state=UserInfoState.age, chat_id=m.chat.id)
        logging.info('[get_name] Move to state AGE')

    else:
        logging.warning(f'[get_name] Invalid name: {m.text}')

        bot.reply_to(message=m, text='Name may consist of letters only')
        bot.set_state(user_id=m.from_user.id, state=UserInfoState.name, chat_id=m.chat.id)


@bot.message_handler(state=UserInfoState.age)
def get_age(m: Message) -> None:
    logging.info(f'[get_age] user={m.from_user.username}, text={m.text}]')

    if not m.text.isdigit():
        logging.warning(f'[get_age] Invalid age: {m.text}')

        bot.reply_to(message=m, text='Uncorrected. Only digits are acceptable ')
        bot.set_state(user_id=m.from_user.id, state=UserInfoState.age, chat_id=m.chat.id)

    else:
        with bot.retrieve_data(user_id=m.from_user.id, chat_id=m.chat.id) as data:
            data['age'] = m.text

            logging.info(f'[get_age] Saved age: {m.text}')

        bot.send_message(chat_id=m.chat.id, text='Where are you originally from?')
        bot.set_state(user_id=m.from_user.id, state=UserInfoState.country, chat_id=m.chat.id)

        logging.info('[get_age] Move to state COUNTRY')


@bot.message_handler(state=UserInfoState.country)
def get_country(m: Message):
    logging.info(f'[get_age] user={m.from_user.username}, text={m.text}]')

    try:
        c = pycountry.countries.lookup(m.text.strip())
    except LookupError:
        return bot.reply_to(message=m, text="Country not found.")

    code = c.alpha_2

    with bot.retrieve_data(user_id=m.from_user.id, chat_id=m.chat.id) as data:
        data["country"] = c.name
        data["country_code"] = code

    cities = get_cities_by_country(code)
    if not cities:
        load_cities_for_country(code, limit=10)  # подгружаем
        cities = get_cities_by_country(code)  # читаем снова

    if not cities:
        return bot.send_message(chat_id=m.chat.id, text="Cities not loaded yet, try later.")

    kb = generate_city_keyboard(cities[:10])
    bot.send_message(m.chat.id, "Choose your city:", reply_markup=kb)
    bot.set_state(user_id=m.from_user.id, state=UserInfoState.city, chat_id=m.chat.id)

    logging.info('[get_country] Move to state CITY')


@bot.callback_query_handler(func=lambda call: call.data.startswith("city_"), state=UserInfoState.city)
def handle_city(call: CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id)
    city = call.data.split("_",1)[1]

    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        data["city"] = city

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"You chose: {city}")
    bot.set_state(user_id=call.from_user.id, state=UserInfoState.phone_num, chat_id=call.message.chat.id)
    bot.send_message(chat_id=call.message.chat.id, text="Last: Can u send me your phone number?", reply_markup=request_contact())


    @bot.message_handler(content_type=['text', 'contact'], state=UserInfoState.phone_num)
    def get_contact(m: Message):
        if m.content_type == 'contact':
            with bot.retrieve_data(user_id=m.from_user.id, chat_id=m.chat.id) as data:

