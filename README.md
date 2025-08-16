# PolyakiBot

**PolyakiBot** is a Telegram bot that runs a step-by-step survey, collecting user data (name, age, country, city, phone) with the ability to skip certain steps and dynamically load a list of cities from a database.


## Features

- **Step-by-step form** powered by a Finite State Machine (FSM)
- **Dynamic city loading** based on the selected country
- **Country detection** with partial match support using `pycountry`
- **Optional step skipping** (e.g., contact sharing)
- **Final summary** of collected data
- **Logging** for debugging and analytics
- **Retry logic** for failed operations (`backoff`)

___


## Tech Stack

- Python 3.11+
- [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/) - Telegram Bot API wrapper
- SQLite - local database for:
    - storing fetched cities ('cities.db')
    - storing user survey results ('users.db')
- [pycountry](https://pypi.org/project/pycountry/) - country lookup and normalization
- [GeoDB Cities API](https://rapidapi.com/wirefreethought/api/geodb-cities/) via RapidAPI — for fetching cities by country
- [python-dotenv](https://pypi.org/project/python-dotenv/) - for environment variable management
- Built-in `logging` for logging

## Project Structure

```text
PolyakiBot/
├── main.py                # Entry point for running the bot
├── loader.py              # Bot and dependencies initialization
├── config.py              # Project configuration
├── backoff.py             # Retry logic
├── load_cities.py         # Script for populating cities database
├── database/              # Database layer
│   ├── bd.py
│   ├── cities.db
│   └── users.db
├── handlers/              # Command and message handlers
│   ├── custom_handlers/
│   │   └── survey.py
│   └── default_handlers/
│       ├── start.py
│       ├── help.py
│       └── echo.py
├── keyboards/             # Bot keyboards
│   ├── inline/
│   │   └── city_loc.py
│   └── reply/
│       └── contact.py
├── states/                # FSM states
│   └── contact_information.py
├── utils/
│   └── set_bot_commands.py
├── requirements.txt       # Project dependencies
├── .env.example           # Example environment configuration
├── LICENSE
└── README.md
```



## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/LizVin19/PolyakiBot
cd PolyakiBot
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a .env file from the example:
```bash
cp .env.example .env
```

In `.env`:
```ini
BOT_TOKEN=your_telegram_bot_token
API_KEY=your_geodb_api_key
API_URL=https://wft-geo-db.p.rapidapi.com/v1/geo/cities
```
BOT_TOKEN — get it from @BotFather in Telegram
API_KEY — get it on RapidAPI GeoDB Cities
API_URL — base URL for the GeoDB API (already set by default)

### 5. Populate the cities database (if empty)
```bash
python load_cities.py
```

### 6. Run the bot
```bash
python main.py
```


## Example Flow
1. User starts the survey with the `/survey` command.  
2. Bot asks for the **name** → only letters are accepted.  
3. Bot asks for the **age** → must be digits (validated, e.g. 1–120).  
4. Bot asks for the **country** → normalized using `pycountry` (partial matches supported).  
5. Bot shows a list of top cities for the chosen country:
   - fetched from **GeoDB API** (RapidAPI) if not in the local database
   - saved into the **SQLite database** for future use
6. Bot asks for the **phone number** → user can share their contact or type *"no"/"skip"*.
7. All collected data is stored in the local `users.db` database.
8. Bot shows a **summary of collected data** and finishes the survey (state cleared).  



## License 
This project is licensed under the [MIT License](LICENSE).
