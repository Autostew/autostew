#!/bin/bash

# Prerequisites:
#sudo useradd -m autostew
#git clone

# Makes a server (tested on ubuntu)
# RUN IT ON THE GIT REPO PATH
# First parameter is hostname

# Set hostname
sudo sed "1s/.*/127.0.0.1 localhost $1/" /etc/hosts
sudo hostname $1
echo $1 | sudo tee /etc/hostname

# Set up SSH access TODO

# Install packages
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
sudo apt-get install lib32gcc1
sudo apt-get install libmysqlclient-dev
sudo pip3 install mysqlclient
sudo pip3 install -r requirements.txt

# Set up steam
sudo useradd -m steam
sudo -u steam mkdir /home/steam/steamcmd
pushd /home/steam/steamcmd
sudo -u steam wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
sudo -u steam tar -xvzf steamcmd_linux.tar.gz
sudo -u steam ./steamcmd.sh +login anonymous +force_install_dir ./pcars_ds +app_update 332670 validate +exit
popd

# Set up DS
sudo -u steam ln -sfn /home/steam/steamcmd/pcars_ds/server.cfg $PWD/devops/server.cfg
sudo cp devops/pcars-ds.service /usr/lib/systemd/system/
sudo systemctl enable pcars-ds.service
sudo systemctl start pcars-ds.service

# Set up apache TODO


# Deploy autostew TODO


# Set up autostew TODO


# Let's go! TODO

