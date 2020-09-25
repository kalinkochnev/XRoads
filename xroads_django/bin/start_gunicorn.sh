#!/bin/bash

cd /home/xroads/xroads_dj

gunicorn xroads_django.wsgi:application --log-file -