# stage1 - build react app first 
FROM nginx:1.21
RUN apk add --no-cache certbot
RUN certbot certonly --standalone -d xroads.club,www.xroads.club --email kalin.kochnev@gmail.com -n --agree-tos --expand

RUN rm /etc/nginx/conf.d/default.conf

COPY compose/production/nginx/nginx.conf /etc/nginx/conf.d

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
