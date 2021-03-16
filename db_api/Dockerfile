FROM redis
MAINTAINER Grzegorz Roguski

EXPOSE 6379

COPY config/redis.conf /redis.conf
CMD [ "redis-server", "/redis.conf" ]
