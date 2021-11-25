# syntax=docker/dockerfile:1

# pull official base image
FROM python:3.10.0-slim-buster AS development_build

# grab arg from docker-compose.yml
ARG DJANGO_ENV

# set env vars
ENV DJANGO_ENV=${DJANGO_ENV} \
  # python
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry
  POETRY_VERSION=1.1.11 \
  # POETRY_VIRTUALENVS_CREATE=false \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# system deps
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
  # cleaning cache
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  # install poetry
  && pip install "poetry==$POETRY_VERSION" && poetry --version

# set work directory
WORKDIR /code

# copy dependencies
COPY pyproject.toml /code/
COPY wheels /code/wheels

# install dependencies
RUN poetry install

# # copy entrypoint.sh
# COPY ./entrypoint.sh .

# copy project
COPY . .

# install netcat, required for nc command in entrypoint.sh
RUN apt-get update && apt-get install -y netcat

# run entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]