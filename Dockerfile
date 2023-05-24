FROM python:3.10-slim

RUN apt -y update && apt -y install curl

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/root/.local/bin:$PATH"

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry env use python3.10 && poetry install

# Copy bot sources
COPY ./ /pht-bot/

CMD poetry env use python3.10 && poetry run python3 /pht-bot/main.py
