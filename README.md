## Public habit tracker

Telegram bot for habit tracking with collaboration features.

**Development stage**: not released yet.

## How to run the bot

### Via Docker

Credentials for Telegram API, Postgresql and Redis are stored in the `.env` file.
There is an almost ready file called `.env.example` for running the bot,
which contains all necessary variables, except for the `BOT_TOKEN`. Just copy
the sample file:

```bash
cp .env.example .env
```

Then you need to change host addresses from `0.0.0.0` to `pht-redis` and `pht-db`
respectively and fill in the `BOT_TOKEN` value with your bot token, that can be obtained
from [BotFather](https://t.me/BotFather).

To run the bot with Postgresql and Redis, run:

```
sudo docker-compose up
```

### Locally (useful for development)

Prerequisites:

- Python 3.10
- [Poetry](https://python-poetry.org/docs/)

You also need Postgresql and Redis to run the bot. You can create Docker
containers with them with these commands:

```bash
docker run -p 5432:5432 --name pht-db -e POSTGRES_DB=pht-db -e POSTGRES_PASSWORD=postgres -d postgres
docker run -d --name pht-redis -p 6379:6379 redis/redis-stack-server:latest
```

After creating containers, you can always start them like this (e.g. after
rebooting):

```bash
docker start pht-redis pht-db
```

Credentials for Telegram API, Postgresql and Redis are stored in the `.env`
file. There is an almost ready file called `.env.example` to run the bot,
which contains all necessary variables, except for the `BOT_TOKEN`. Just copy
the sample file:

```bash
cp .env.example .env
```

Then fill in the `BOT_TOKEN` value with your bot token, that can be obtained
from [BotFather](https://t.me/BotFather). If you've created Postgresql and Redis
containers with instructions above, then other variables are already set correct.

To run the bot with poetry virtual environment, run:

```bash
poetry env use 3.10
poetry install
poetry run python main.py
```

You also can use the standard Python's `venv` module instead of poetry's
virtual environment:

```bash
sudo apt install python3.10 python3.10-venv
python3.10 -m venv venv
source venv/bin/activate
poetry install
python main.py
```

### Development notes

If you want to contribute to this project, feel free to send pull requests.
This project uses [black](https://github.com/psf/black),
"The Uncompromising Code Formatter". Please, format
your code with it before submitting a PR. You can easily set up a file
watcher in your IDE to format the code with `black` every time you save a file.

A useful command for recreating the database:

```
# this command will DROP ALL DATA from the db
docker exec -it pht-db /bin/bash -c "dropdb -f -U postgres pht-db; createdb -U postgres pht-db"
```

### TODO

- GH actions: black, flake8, (pytest?)
