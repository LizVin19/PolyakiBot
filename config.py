import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('переменные среды не загружены. файл .env не найден')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEFAULT_COMMANDS = (
    ('start', 'bot run'),
    ('help', 'help me'),
    ('survey', 'ask me')
)


# GeoDB
API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')
API_HOST = "wft-geo-db.p.rapidapi.com"