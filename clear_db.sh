#!/bin/bash
rm -rf db.sqlite3
rm -rf **/migrations
python manage.py makemigrations g1
python manage.py makemigrations g2
python manage.py makemigrations g3
python manage.py makemigrations g4
python manage.py makemigrations main
python manage.py makemigrations mypage
python manage.py migrate
