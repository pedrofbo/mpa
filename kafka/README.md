# Apache Kafka Docker POC

The following files provide a simple implementation of Apache Kafka running
on docker and two Python scripts to produce and consume data from it.

The files available here were based on the following tutorials:
- [Confluent - Kafka quickstart using Docker](https://developer.confluent.io/quickstart/kafka-docker/)
- [Confluent - Kafka Python Client quickstart](https://docs.confluent.io/kafka-clients/python/current/overview.html#ak-python)

## Setup
- You must have Docker and docker-compose installed.
- Your Python running environment must install the packages in `requirements.txt`.

## Running
- The `start.sh` script will start/restart the Kafka broker and create a
`quickstart` topic.
- The `producer_example.py` script will publish a single message to said topic when ran.
- The `consumer_example.py` script will listen for messages published on said
topic until manually interrupted.
