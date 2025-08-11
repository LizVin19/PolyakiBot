import logging
import time

import requests
from config import API_URL, API_KEY, API_HOST
from database.bd import insert_cities
from backoff import get_with_retries

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)5s %(message)s',
    datefmt='%H:%M:%S'
)


HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST
}


def load_cities_for_country(country_code: str, limit: int = 10):
    """
    Скачиваем топ-`limit` городов для страны с кодом country_code
    и сохраняем их в таблицу cities через insert_cities().
    """
    params = {
        'countryIds': country_code,
        'limit': limit,
        'sort': '-population'
    }

    # resp = requests.get(API_URL, headers=HEADERS, params=params)
    resp = get_with_retries(API_URL, headers=HEADERS, params=params)
    if resp is None:
        return []
    if resp.status_code != 200:
        logging.error(f'[LOAD_CITIES] GeoDB API error {resp.status_code}: {resp.text}')
        return []

    data = resp.json().get('data', [])
    if not data:
        logging.warning(f'[LOAD_CITIES] Not found cities for {country_code}')
        return []

    insert_cities(data)
    logging.info(f'[LOAD_CITIES] Inserted {len(data)} cities for {country_code}')
    return data


if __name__ == '__main__':
    load_cities_for_country('RU', limit=10)
    time.sleep(1)
    load_cities_for_country('KZ', limit=10)
    time.sleep(1)
    load_cities_for_country('GE', limit=10)

