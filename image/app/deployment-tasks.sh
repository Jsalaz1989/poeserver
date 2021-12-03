#!/bin/sh

xargs -a .env -I {} heroku config:set {}

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
