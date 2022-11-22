from prometheus_client import Gauge

level = Gauge(
    "mpa_trainers_pokemon_level",
    "Level of a given trainer's pokemon",
    ["trainer", "pokemon"])


def handler(message: dict):
    trainer = message["response"]["trainer"]
    pokemon = message["response"]["name"]
    new_level = message["response"]["level"]
    level.labels(trainer=trainer, pokemon=pokemon).set(new_level)
