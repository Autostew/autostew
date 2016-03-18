#!/bin/bash
rm -vrf autostew_web_enums/migrations/* autostew_web_session/migrations/* autostew_web_users/migrations/* db.sqlite3
./manage.py makemigrations autostew_web_session autostew_web_enums autostew_web_users
./manage.py migrate
echo "New admin password (username admin)"
./manage.py createsuperuser --username=admin --email='none@localhost'
