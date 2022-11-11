import json
import logging
import os
import time
from datetime import datetime
from functools import wraps

from confluent_kafka import Producer
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)-8s - %(message)s"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

_producer = None


def _setup_producer():
    global _producer
    if _producer is None:
        endpoint = os.environ.get("KAFKA_ENDPOINT", "localhost:19092")
        conf = {"bootstrap.servers": endpoint}
        _producer = Producer(conf)


def _callback(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(
            f"Message '{msg.value().decode('utf-8')}' delivered to topic "
            f"{msg.topic()}."
        )


def _push_message(message: dict, topic: str):
    try:
        _setup_producer()
        message = json.dumps(message)
        _producer.produce(topic, value=message, callback=_callback)
        _producer.poll(1)
    except Exception as e:
        logger.error(f'Failed to push message "{message}" to Kafka. '
                     f'Error - {str(e)}')


def kafka_logging(topic: str):

    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            response = await method(*args, **kwargs)
            elapsed_time = time.time() - start_time
            message = {
                "endpoint": "/" + topic.lower().replace("__", "/"),
                "response_status": response.status_code,
                "response": json.loads(response.body.decode('utf-8')),
                "start_time": datetime.fromtimestamp(start_time),
                "elapsed_time": elapsed_time
            }
            _push_message(jsonable_encoder(message), topic)
            return response

        return wrapper

    return decorator
