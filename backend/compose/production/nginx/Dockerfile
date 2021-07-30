# stage1 - build react app first 
FROM nginx:1.21
RUN rm /etc/nginx/conf.d/default.conf

COPY compose/production/nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
