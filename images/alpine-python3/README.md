
# Python Runner

This is a Docker image to run Python scripts.

```bash
docker build -t ipirva/alpine-python:latest -t alpine-python:alpine3.18.4 --no-cache .
docker image tag ipirva/alpine-python ipirva/alpine-python:alpine3.18.4
docker image push --all-tags ipirva/alpine-python
```