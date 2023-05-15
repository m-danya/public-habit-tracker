FROM ubuntu:20.04

# Install python 3.10 and poetry
RUN apt update && apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt -y install python3.10 pip && pip install poetry

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry env use python3.10 && poetry install

WORKDIR /pht-bot

CMD poetry env use python3.10 && poetry run python3 src/main.py
