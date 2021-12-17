#!/bin/sh

python manage.py makemigrations
python manage.py migrate
ls -a .
# python manage.py collectstatic
# python manage.py test
