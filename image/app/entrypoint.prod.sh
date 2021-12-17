#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

which python
ls -a .

gunicorn server.wsgi:application --bind 0.0.0.0:$PORT --reload --log-level debug --access-logfile - --error-logfile -

# exec "$@"