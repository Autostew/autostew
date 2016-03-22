#! /bin/bash

SETTINGS_ROOT=autostew.settings

if [ $# -eq 0 ]
then
	echo "You need to provide an environment"; exit;
else
	export DJANGO_SETTINGS_MODULE=$SETTINGS_ROOT.$1
fi
