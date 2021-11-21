#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# poetry run python manage.py flush --no-input
# poetry run python manage.py migrate

# poetry env info

. .venv/bin/activate

which python
# ls -a .venv/lib/python3.10/site-packages
# ls -la .venv/bin

ls -a ./server
gunicorn --version

exec "$@"