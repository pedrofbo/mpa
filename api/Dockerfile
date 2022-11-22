FROM python:3.9-slim-buster

WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt
COPY ./server.py ./server.py
COPY ./models.py ./models.py
COPY ./database.py ./database.py
COPY ./kafka.py ./kafka.py

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
