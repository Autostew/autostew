#!/bin/sh

git checkout -b docker-instance
git fetch
git checkout autostew/settings/common.py
git merge origin/$1

./autostew_back.py -i $2
