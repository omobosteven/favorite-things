#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y

echo "Installing python...."
{
	sudo apt-get install python3-pip -y
	sudo apt-get install python3.7 -y
	echo "Python Installed :)"
} || {
	echo "Python installation failed"
}

echo "Installing pipenv..."
{
	echo 'export PATH="${HOME}/.local/bin:$PATH"' >> ~/.bashrc
	source ~/.bashrc
	sudo python3.7 -m pip install --user pipenv
	echo "Pipenv installed :)"
} || {
	echo "Pipenv installation failed"
}

echo "Installing nodejs"
{
	sudo apt-get install wget
	wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
	source ~/.bashrc
	nvm install 11.12.20
	echo "Node installed :)"
} || {
	echo "Nodejs installation failed"
}

echo "Installing client dependencies"
make npm-install
echo "Dependencies installed :)"

echo "building client"
make build-client
echo "client built :)"

echo "Installing server depenedencies"
	make pipenv-install
	pipenv run make migrate
	pipenv run start-gunicorn
echo "Gunicorn server started"

echo "Installing Nginx"
sudo apt-get install nginx -y
sudo touch /etc/nginx/sites-available/favorite_things
sudo ln -s /etc/nginx/sites-available/favorite_things /etc/nginx/sites-enabled/favorite_things

sudo cp nginx.conf /etc/nginx/nginx.conf
sudo cp favorite_things /etc/nginx/sites-available/favorite-things
sudo nginx -t
sudo service nginx restart

