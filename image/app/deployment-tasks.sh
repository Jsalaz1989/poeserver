#!/bin/sh

python manage.py makemigrations --merge
python manage.py migrate
