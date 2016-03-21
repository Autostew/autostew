#!/bin/bash
rm -vrf autostew_web_enums/migrations/* autostew_web_session/migrations/* autostew_web_users/migrations/* db.sqlite3
./manage.py makemigrations autostew_web_session autostew_web_enums autostew_web_users --settings=autostew.settings.dev
./manage.py migrate --settings=autostew.settings.dev
echo "New admin password (username admin)"
./manage.py createsuperuser --username=admin --email='none@localhost' --settings=autostew.settings.dev
