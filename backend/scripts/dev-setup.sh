#!/bin/bash
# Make sure to run     chmod a+x install.sh     before running
# To execute  ./install.sh
# Make sure this is run at the root directory

if ! command -v python3-pip &> /dev/null
then
    echo "Installing pip.................................."
    sudo apt-get install python3-pip -y > /dev/null
fi

if ! command -v python3-venv &> /dev/null
then
    echo "Installing venv.................................."
    sudo apt-get install python3-venv -y > /dev/null
fi


FILE=xroads_django/venv/
if [! -f "$FILE" ]; then
    echo "The virtual env was not setup."
    python3 -m venv xroads_django/venv/ > /dev/null
fi

echo "Installing pip packages.................................."
. ./xroads_django/venv/bin/activate
pip3 --version
pip3 install -r xroads_django/requirements.txt

echo "Installing postgres.................................."
sudo apt update > /dev/null
sudo apt install postgresql postgresql-contrib -y > /dev/null

password="PTUvEj9Bh9P2"

setup_db_command="
    create database xroadsdb;
    create user djangouser with encrypted password '$password';
    alter user djangouser with encrypted password '$password';
    grant all privileges on database xroadsdb to djangouser;
    alter user djangouser CREATEDB;
    \q
"
echo ${setup_db_command}
sudo -u postgres psql <<< $setup_db_command

# Install npm
echo "Setting up npm.................................."
sudo apt-get install npm
cd frontend/
npm install
npm audit fix
