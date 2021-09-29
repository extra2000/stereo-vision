FROM docker.io/python:3.9.7-slim-bullseye

VOLUME /root/.cache/pip
VOLUME /opt/source

COPY . /opt/source/
WORKDIR /opt/source

RUN python -m pip install .

WORKDIR /opt/workdir
