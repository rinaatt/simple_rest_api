FROM redis:latest

RUN mkdir -p /etc/redis
ADD redis.conf /etc/redis/redis.conf

CMD [ "redis-server", "/etc/redis/redis.conf" ]
