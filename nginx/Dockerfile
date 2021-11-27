FROM nginx:1.15.8
RUN rm -f /etc/nginx/conf.d/*
ADD nginx.conf /etc/nginx/conf.d/nginx.conf
COPY static/ /app/static/

CMD /usr/sbin/nginx -g 'daemon off;' -c /etc/nginx/nginx.conf