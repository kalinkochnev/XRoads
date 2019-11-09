#!/bin/bash
# Make sure to run     chmod a+x install.sh     before running
# To execute  ./install.sh

sudo apt update
sudo apt install postgresql postgresql-contrib

sudo -u postgres psql << EOF
    create database xroadsdb;
    create user djangouser with encrypted password 'password';
    grant all privileges on database xroadsdb to djangouser;
