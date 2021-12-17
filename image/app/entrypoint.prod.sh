#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# echo $PWD
# ls -a $PWD
# ls -a home/app/web
# . .venv/bin/activate
which python
# ls -a .venv/lib/python3.10/site-packages
# ls -la .venv/bin
# ls -a ./server
# gunicorn --version

gunicorn server.wsgi:application --bind 0.0.0.0:$PORT --reload --log-level debug --access-logfile - --error-logfile -

# exec "$@"