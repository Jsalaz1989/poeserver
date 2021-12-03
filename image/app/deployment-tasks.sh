#!/bin/sh

ls -a .
# xargs -a .env.prod -I {} heroku config:set {}

python manage.py makemigrations
python manage.py migrate
# python manage.py collectstatic
