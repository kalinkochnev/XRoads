#!/bin/bash
# Make sure to run     chmod a+x install.sh     before running
# To execute  ./install.sh

sudo apt install python3-pip
pip3 --version
pip3 install -r requirements.txt

sudo apt update
sudo apt install postgresql postgresql-contrib

password="PTUvEj9Bh9P2"
sudo -u postgres psql << EOF
    create database xroadsdb;
    create user djangouser with encrypted password '$password';
    alter user djangouser with encrypted password '$password';
    grant all privileges on database xroadsdb to djangouser;