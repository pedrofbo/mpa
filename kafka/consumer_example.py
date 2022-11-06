from confluent_kafka import Consumer, KafkaException

conf = {'bootstrap.servers': "localhost:9092",
        'group.id': "test",
        'auto.offset.reset': 'smallest'}
consumer = Consumer(conf)


def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            if msg.error():
                raise KafkaException(msg.error())
            else:
                print(msg.value().decode("utf-8"))
    finally:
        consumer.close()


if __name__ == "__main__":
    topics = ["quickstart"]
    basic_consume_loop(consumer, topics)
