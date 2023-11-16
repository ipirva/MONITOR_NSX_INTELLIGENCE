FROM alpine:3.18.4

ENV TZ Etc/UTC
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/bin

RUN apk add --update --no-cache python3 py3-requests && ln -sf python3 /usr/bin/python && rm -vrf /var/cache/apk/*
CMD ["/bin/sh"]