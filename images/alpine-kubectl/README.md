
# kubectl Runner

This is a Docker image to run kubectl.

```bash
docker build -t ipirva/alpine-kubectl:latest -t alpine-python:kubectl1.28.4 --no-cache .
docker image tag ipirva/alpine-kubectl ipirva/alpine-kubectl:kubectl1.28.4
docker image tag ipirva/alpine-kubectl ipirva/alpine-kubectl:alpine3.18.4
docker image push --all-tags ipirva/alpine-kubectl
```