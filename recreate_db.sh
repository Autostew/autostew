#!/bin/bash
rm -vrf autostew_web_enums/migrations/* autostew_web_session/migrations/* autostew_web_users/migrations/* autostew_web_contact/migrations/* db.sqlite3
./manage.py makemigrations autostew_web_session autostew_web_enums autostew_web_users autostew_web_contact
./manage.py migrate
