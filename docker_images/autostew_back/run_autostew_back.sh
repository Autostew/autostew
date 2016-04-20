#!/bin/sh

cd autostew
git checkout $1
git pull

./autostew_back.py -i $2
