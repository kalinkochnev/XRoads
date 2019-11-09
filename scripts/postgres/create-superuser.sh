#!/bin/bash

echo 'Enter a username: \n'
read USERNAME
echo 'Enter a password: \n'
read PASSWORD

sudo -u postgres psql << EOF
    create user $USERNAME with encrypted password '$PASSWORD';
    grant all privileges on database xroadsdb to $USERNAME;
