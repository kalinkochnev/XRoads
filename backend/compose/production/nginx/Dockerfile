# stage1 - build react app first 
FROM nginx:1.21
RUN apt-get update
RUN apt-get install -y certbot
RUN apt-get install -y python3-certbot-nginx

EXPOSE 80
RUN rm /etc/nginx/conf.d/default.conf
COPY compose/production/nginx/nginx.conf /etc/nginx/conf.d/xroads.club.conf
# CMD ["nginx", "-g", "daemon off;"]

COPY compose/production/nginx/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
