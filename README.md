# PolyakiBot

**PolyakiBot** is a Telegram bot that runs a step-by-step survey, collecting user data (name, age, country, city, phone) with the ability to skip certain steps and dynamically load a list of cities from a database.


## Features

- **Step-by-step form** powered by a Finite State Machine (FSM)
- **Dynamic city loading** based on the selected country
- **Country detection** with partial match support using `pycountry`
- **Optional step skipping** (e.g., contact sharing)
- **Final summary** of collected data
- **Logging** for debugging and analytics
- **Retry logic** for failed operations (`backoff`

___


## Tech Stack

- Python 3.11+
- [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
- SQLite (for users and cities storage)
- [pycountry](https://pypi.org/project/pycountry/)
- [GeoDB Cities API](https://rapidapi.com/wirefreethought/api/geodb-cities/) via RapidAPI — for fetching cities by country
- [python-dotenv](https://pypi.org/project/python-dotenv/) - for environment variable management
- Built-in `logging` for logging

## Project Structure

```text
├```text
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
USERS_DB_PATH=./database/users.db
CITIES_DB_PATH=./database/cities.db
```
### 5. Populate the cities database (if empty)
```bash
python load_cities.py
```

### 6. Run the bot
```bash
python main.py
```


## Example Flow
1. User enters their name
2. Enters age
3. Selects country (partial matching supported)
4. Selects city from dynamically loaded list
5. Sends contact or skips
6. Receives a final summary of their input


## License 
This project is licensed under the [MIT License](LICENSE).
