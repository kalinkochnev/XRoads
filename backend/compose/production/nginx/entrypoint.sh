#!/bin/sh

certbot --nginx -d xroads.club,www.xroads.club --email kalin.kochnev@gmail.com -n --agree-tos --expand

nginx -d daemon off;