FROM python:3.9-slim-buster

WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt
COPY ./fast_server.py ./fast_server.py
COPY ./models.py ./models.py
COPY ./database.py ./database.py

RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
