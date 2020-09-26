#!/bin/bash

deployDir = $(pwd)

cd $deployDir/xroads_django && podman build . -t localhost/django_gunicorn

cd $deployDir/xroads_react && npm run build

cd $deployDir/nginx && podman build . -t django_nginx