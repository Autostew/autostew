git clone https://github.com/Autostew/autostew.git
cd autostew

apt-get -y install python3-pip
apt-get -y install lib32gcc1
apt-get -y install libmysqlclient-dev
pip3 install mysqlclient
pip3 install -r requirements.txt