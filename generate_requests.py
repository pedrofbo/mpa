import random
import time
from uuid import uuid4

import requests

endpoint = "http://localhost:8080"
configuration = {
    "pokemon": {
        "type": "GET",
        "endpoint": "/pokemon/{id}",
        "ids": list(range(1, 906))
    },
    "random_pokemon": {
        "type": "GET",
        "endpoint": "/pokemon/random",
        "ids": None
    },
    "trainers": {
        "type": "GET",
        "endpoint": "/trainers/{id}",
        "ids": ["ash", "bob", "Marco", "Melo"]
    },
    "trainer_pokemon": {
        "type": "GET",
        "endpoint": "/trainers/{id}/pokemon",
        "ids": ["ash", "bob", "Marco", "Melo"]
    },
    "register_pokemon": {
        "type": "POST",
        "endpoint": "/trainers/bob/pokemon",
        "ids": list(range(1, 906))
    },
    "level_pokemon_ash": {
        "type": "POST",
        "endpoint": "/trainers/ash/pokemon/{id}/level",
        "ids": ["dracovish", "dragonite", "gengar",
                "lucario", "pikachu", "sirfetchd"]
    },
    "level_pokemon_red": {
        "type": "POST",
        "endpoint": "/trainers/red/pokemon/{id}/level",
        "ids": ["blastoise", "charizard", "lapras",
                "pikachu", "snorlax", "venusaur"]
    },
    "invalid_pokemon": {
        "type": "GET",
        "endpoint": "/pokemon/{id}",
        "ids": list(range(906, 910))
    },
    "invalid_trainers": {
        "type": "GET",
        "endpoint": "/trainers/{id}",
        "ids": ["ayo", "idontexist", "sheesh"]
    }
}


def register_pokemon(id_: int, url: str) -> dict:
    body = {
        "id": id_,
        "nickname": uuid4().hex,
        "level": random.randrange(1, 60)
    }
    response = requests.post(url, json=body)
    return response


def level_pokemon(url: str) -> dict:
    body = {
        "levels": random.randrange(-2, 3)
    }
    response = requests.post(url, json=body)
    return response


def run():
    request_setup = configuration[random.choice(list(configuration.keys()))]
    if request_setup["type"] == "GET":
        if request_setup["ids"] is not None:
            id_ = random.choice(request_setup["ids"])
            url = request_setup["endpoint"].format(id=id_)
        else:
            url = request_setup["endpoint"]
        url = endpoint + url
        response = requests.get(url)
    else:
        id_ = random.choice(request_setup["ids"])
        if request_setup["endpoint"] == "/trainers/bob/pokemon":
            url = endpoint + request_setup["endpoint"]
            response = register_pokemon(id_, url)
        elif "/pokemon/{id}/level" in request_setup["endpoint"]:
            url = endpoint + request_setup["endpoint"].format(id=id_)
            response = level_pokemon(url)
    print(request_setup["type"])
    print(url)
    print(response.json())


if __name__ == "__main__":
    while True:
        run()
        interval = random.uniform(0, 5)
        print(interval)
        time.sleep(interval)
