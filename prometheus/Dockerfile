FROM python:3.9.13-slim-buster

WORKDIR /usr/src/app

COPY ./requirements.txt ./
COPY ./kafka.py ./
COPY ./metric_handlers ./metric_handlers

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT python kafka.py
