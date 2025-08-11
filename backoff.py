import logging
import time
import requests


def get_with_retries(url, headers, params, max_attempts=5, base_delay=1.0):
    for attempt in range(1, max_attempts + 1):
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 200:
            return resp
        if resp.status_code == 429:
            retry_after = resp.headers.get('Retry-After')
            if retry_after:
                delay = float(retry_after)
            else:
                delay = base_delay * (2 ** (attempt- 1)) + (0.1 * attempt)
            logging.warning(f'[LOAD_CITIES] Rate limited (429), sleeping {delay:.1f}s (attempt {attempt})')
            time.sleep(delay)
            continue

        logging.error(f'[LOAD_CITIES] GeoDB API error {resp.status_code}: {resp.text}')
        return resp
    logging.error(f'[LOAD_CITIES] Exhausted retries after {max_attempts} attempts due to rate limiting')
    return None

