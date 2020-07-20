#!/bin/bash
# Make sure to run     chmod a+x install.sh     before running
# To execute  ./install.sh

sudo -u postgres psql << EOF
    DROP DATABASE IF EXISTS xroadsdb;
    create database xroadsdb;
    grant all privileges on database xroadsdb to djangouser;