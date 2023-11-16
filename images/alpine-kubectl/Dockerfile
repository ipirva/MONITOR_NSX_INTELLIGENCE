FROM alpine:3.18.4

ENV TZ Etc/UTC
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/bin

RUN \
    apk add --update --no-cache curl && rm -vrf /var/cache/apk/* && \
    # latest stable to date v1.28.4
    # https://storage.googleapis.com/kubernetes-release/release/stable.txt
    curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.28.4/bin/linux/amd64/kubectl && \
    chmod +x kubectl && mv kubectl /usr/local/bin
CMD ["/bin/sh"]