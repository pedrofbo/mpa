FROM python:3.9-slim-buster

WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt
COPY ./server.py ./server.py

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "0", "--timeout", "0", "server:app"]
