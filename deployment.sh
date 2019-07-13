#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install python3.7-pip -y
sudo apt-get install python3.7 -y
sudo apt-get install libpq-dev -y
sudo apt-get install postgresql -y
sudo apt-get install postgresql-contrib -y
sudo apt-get install nginx -y
sudo apt-get install git -y

echo 'export PATH="${HOME}/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
sudo python3.7 -m pip install --user pipenv

sudo apt-get install wget
wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
source ~/.bashrc

nvm install 11.12.20

make pipenv-install
pipenv shell
make migrate
make start-gunicorn

make npm-install
make build-client
sudo touch /etc/nginx/sites-available/favorite_things
sudo ln -s /etc/nginx/sites-available/favorite_things /etc/nginx/sites-enabled/favorite_things

cp nginx.conf /etc/nginx/nginx.conf
cp favorite_things /etc/nginx/sites-available/favorite-things

sudo nginx -t
sudo service nginx restart
