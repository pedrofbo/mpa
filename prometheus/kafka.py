import json
import os
import time
import logging

from confluent_kafka import Consumer, KafkaException
from prometheus_client import start_http_server, Counter, Gauge

from metric_handlers import (
    pokemon__random, trainers__name__pokemon__name__level__register
)

# Logging setup
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)-8s - %(message)s"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel("INFO")

# Kafka topics setup
topics_path = os.environ.get("TOPICS_PATH", "../topics.txt")
with open(topics_path) as f:
    topics_file = f.read()
topics: list = topics_file.strip().split("\n")

counter = Counter(
    "mpa_requests_total",
    "Request count for the MPA API",
    ["endpoint", "request_type", "status_code"])

gauge = Gauge(
    "mpa_request_response_time",
    "Response time for endpoints on the MPA API",
    ["endpoint", "request_type", "status_code"]
)


def handle_message(message: dict):
    endpoint = message["endpoint"]
    request_type = message["request_type"]
    status = message["response_status"]
    counter.labels(endpoint=endpoint, request_type=request_type,
                   status_code=status).inc()
    gauge.labels(
        endpoint=endpoint, request_type=request_type,
        status_code=status).set(message["elapsed_time"])

    if endpoint == "/pokemon/random":
        pokemon__random.handler(message)
    if endpoint == "/trainers/name/pokemon/name/level/register":
        trainers__name__pokemon__name__level__register.handler(message)


def consumer_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            if msg.error():
                raise KafkaException(msg.error())
            else:
                value = json.loads(msg.value().decode("utf-8"))
                logger.info(f'{msg.topic()} - {value}')
                handle_message(value)
    finally:
        consumer.close()


def _setup_consumer():
    kafka_endpoint = os.environ.get("KAFKA_ENDPOINT", "localhost:19092")
    conf = {'bootstrap.servers': kafka_endpoint,
            'group.id': "test",
            'auto.offset.reset': 'smallest'}
    consumer = Consumer(conf)

    return consumer


if __name__ == "__main__":
    start_http_server(8000)

    retries = 0
    while True:
        try:
            consumer = _setup_consumer()
            logger.info(f"Listening to topics - {topics}")
            consumer_loop(consumer, topics)
        except Exception as e:
            logger.error(str(e))
            retries = retries + 1
            if retries > 5:
                break
            time.sleep(30)
