#!/bin/sh

apt-get -y update
apt-get -y upgrade

apt-get -y install git python3 python3-pip

git clone https://github.com/Autostew/autostew.git

cd autostew
pip3 install -r requirements.txt
