FROM nginx:1.12-alpine

RUN mkdir /var/www

RUN rm /etc/nginx/conf.d/default.conf
ADD rest.nginx /etc/nginx/conf.d/rest.conf
ADD rest_admin.nginx /etc/nginx/conf.d/rest_admin.conf
