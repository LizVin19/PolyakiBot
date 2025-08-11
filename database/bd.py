import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
USERS_DB = BASE_DIR / 'users.db'
CITIES_DB = BASE_DIR / 'cities.db'


def init_users_db():
    conn = sqlite3.connect(USERS_DB)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        telegram_id INTEGER, 
        name TEXT,
        age INTEGER,
        country TEXT,
        country_code TEXT,
        city TEXT,
        phone TEXT
    )
    ''')
    conn.commit()
    conn.close()


def save_user(telegram_id: int, name: str, age: int,
              country: str, country_code: str, city: str, phone: str):
    conn = sqlite3.connect(USERS_DB)
    c = conn.cursor()
    c.execute('''
    INSERT INTO users (telegram_id, name, age, country, country_code, city, phone)
    VALUES ( ?, ?, ?, ?, ?, ?, ?) 
    ''', (telegram_id, name, age, country, country_code, city, phone))
    conn.commit()
    conn.close()


def init_cities_db():
    conn = sqlite3.connect(CITIES_DB)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        country_code TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


def insert_cities(cities: list[dict]):
    '''
    Rewrites the cities.db table, saves the name and country code from lists
    of dicts from GeoDB.
    '''
    conn = sqlite3.connect(CITIES_DB)
    c = conn.cursor()
    c.execute('DELETE FROM cities')

    for city in cities:
        c.execute('''
            INSERT INTO cities (name, country_code)
            VALUES (?, ?)
        ''', (city['name'], city['countryCode'].upper()))
    conn.commit()
    conn.close()

def get_cities_by_country(country_code: str) -> list[str]:
    country_code = country_code.upper()
    conn = sqlite3.connect(CITIES_DB)
    c = conn.cursor()
    c.execute(
        'SELECT name FROM cities WHERE country_code = ? ORDER BY name',
        (country_code,)
    )
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows] if rows else []
