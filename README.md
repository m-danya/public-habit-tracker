## Public habit tracker

Telegram bot for habit tracking with collaboration features

**Development stage**: very early

## Run bot

### Via Docker

TBD

### Locally

Prerequisites:
- Python 3.10
- poetry

```bash
docker run -p 5433:5432 --name pht-db -e POSTGRES_DB=pht-db -e POSTGRES_PASSWORD=postgres -d postgres
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
cp .env.example .env
vim .env # at least, change BOT_TOKEN to yours
poetry run python app.py
```

### TODO
- Dockerfile
- GH actions: black, flake8, (pytest?)
- Migrations?
- dev readme: black, ...
