#!/bin/sh

git checkout -b docker-instance
git fetch
git merge origin/$1

./autostew_back.py -i $2
