# syntax=docker/dockerfile:1

### VENV ###
FROM python:3.10.0-slim-buster AS venv

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
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# set paths
ENV APP_HOME=/home/app/web
ENV VIRTUAL_ENV=$APP_HOME/.venv

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
    unzip \
  # clean cache
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  # install poetry
  && pip install "poetry==$POETRY_VERSION" && poetry --version

# set work directory
WORKDIR $APP_HOME

# copy dependencies
COPY pyproject.toml $APP_HOME
COPY wheels $APP_HOME/wheels

# The `--copies` option tells `venv` to copy libs and binaries instead of using links 
# (which could break since we will extract the virtualenv from this image)
RUN python -m venv --copies $VIRTUAL_ENV
RUN . $VIRTUAL_ENV/bin/activate && poetry install


### BASE ###
FROM python:3.10.0-slim-buster as base

# set paths
ENV APP_HOME=/home/app/web
ENV VIRTUAL_ENV=$APP_HOME/.venv
ENV PATH="$APP_HOME:$VIRTUAL_ENV/bin:$PATH"

# create the app user
RUN adduser --system --group app

# create the appropriate directories
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# copy project
COPY . $APP_HOME

# copy venv from previous stage
COPY --from=venv $VIRTUAL_ENV $VIRTUAL_ENV

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# install netcat, required for nc command in entrypoint.sh
RUN apt-get update && apt-get install -y netcat


### PROD ###
FROM base AS prod

RUN rm -r $APP_HOME/staticfiles
RUN rm -r $APP_HOME/mediafiles
  
# required by Heroku
RUN chmod +x entrypoint.prod.sh && \
    chmod +x deployment-tasks.sh && \
    apt-get update && apt-get install -y curl

# change to the app user
USER app

ENTRYPOINT ["entrypoint.prod.sh"]

### DEV / QA / STAGING ###
FROM base AS dev

# system deps
RUN apt-get update && \
  apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
    unzip

# download geckodriver
RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /home/app/web/firefox && \
    chmod +x /home/app/web/firefox/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz
ENV PATH="$APP_HOME/firefox:$PATH"

RUN FIREFOX_SETUP=firefox-95.0.tar.bz2 && \
    apt-get update && apt-get purge firefox && apt-get install --no-install-recommends -y \
      wget bzip2 packagekit-gtk3-module libx11-xcb1 libdbus-glib-1.2 && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP

# change to the app user
USER app

ENTRYPOINT ["entrypoint.dev.sh"]
