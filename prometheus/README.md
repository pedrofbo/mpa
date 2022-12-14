# Prometheus

Proof of concept server that receives messages from a Kafka broker, converts
them to Prometheus metrics and exposes them over an http server at the
`/metrics` endpoint. These metrics are scraped by [Prometheus](https://prometheus.io/)
and are made available for visualization through [Grafana](https://grafana.com/).

## Getting Started

The easiest way to get started with the server, Prometheus and Grafana stack is
to use docker and docker-compose. However, in order for the server to operate
correctly, a Kafka broker must already be running. The most optimal way to
get started with this stack is to simply run the `start.sh` script in the
root of this repository.
