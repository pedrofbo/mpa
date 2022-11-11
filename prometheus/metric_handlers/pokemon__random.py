from prometheus_client import Counter

request_count = Counter(
    "mpa_pokemon__random_request_count",
    "Request count to the /pokemon/random endpoint on the MPA API.",
    ["id", "status_code"])


def handler(message: dict):
    pokemon_id = message["response"]["id"]
    status_code = message["response_status"]
    request_count.labels(id=pokemon_id, status_code=status_code).inc()
