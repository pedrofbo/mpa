from confluent_kafka import Producer

conf = {"bootstrap.servers": "localhost:9092"}
producer = Producer(conf)


def callback(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(
            f"Message '{msg.value().decode('utf-8')}' delivered to topic "
            f"{msg.topic()}"
        )


def deliver(message, topic):
    producer.produce(topic, value=message, callback=callback)
    producer.poll(1)


if __name__ == "__main__":
    deliver("coolio message", "quickstart")
    producer.flush(10)
