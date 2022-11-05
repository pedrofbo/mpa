from datetime import datetime

import firebase_admin
import numpy as np
import requests
from firebase_admin import firestore
from flask import Flask, request

app = Flask(__name__)
firestore_app = firebase_admin.initialize_app(
    options={"projectId": "hotaru-gcp"}
)


def get_pokemon(number: str) -> dict:
    """Retrieve info on the PokeAPI, given a pokemon ID number."""
    url = f"https://pokeapi.co/api/v2/pokemon/{number}"
    response = requests.get(url).json()
    pokemon = {
        "id": response["id"],
        "name": response["name"],
        "artwork": response["sprites"]["other"]["official-artwork"]["front_default"]  # noqa: E501
    }
    return pokemon


@app.route("/pokemon/<number>")
def get_pokemon_from_number(number: str) -> tuple:
    """Given a Pokemon ID, retrieve info about it."""
    pokemon = get_pokemon(number)
    return (pokemon, 200)


@app.route("/pokemon/random")
def get_random_pokemon() -> tuple:
    """Retrieve info for a random pokemon."""
    number = str(np.random.randint(1, 905))
    pokemon = get_pokemon(number)
    return (pokemon, 200)


@app.route("/trainers/<trainer>")
def get_trainer(trainer: str) -> tuple:
    """Retrieve info on Firestore for a given trainer."""
    db = firestore.client(firestore_app)
    doc = db.collection("trainers").document(trainer).get()
    if doc.exists:
        data = doc.to_dict()
        return (data, 200)
    else:
        return (f"Trainer '{trainer}' not found.\n", 404)


@app.route("/trainers", methods=["POST"])
def register_trainer() -> tuple:
    """Register given trainer on Firestore."""
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        request_data = request.json
        if (
            request_data.get("name") is None or
            request_data.get("image") is None
        ):
            return (
                "Json body must contain the 'name' and 'image' keys.\n", 400)
        return _register_trainer(request_data)
    else:
        return ("Content-Type is not of type application/json", 400)


def _register_trainer(data: dict) -> tuple:
    db = firestore.client(firestore_app)
    doc = db.collection("trainers").document(data["name"])
    if not doc.get().exists:
        data = {
            "name": data["name"],
            "image": data["image"],
            "registered_at": datetime.now()
        }
        doc.set(data)
        return ("Trainer registered successfully.\n", 200)
    else:
        return (f"Trainer '{data['name']}' already registered.\n", 404)


@app.route("/trainers/<trainer>/pokemon")
def get_trainer_pokemon(trainer: str) -> tuple:
    """Retrieve a list of pokemon on Firestore for a given trainer."""
    db = firestore.client(firestore_app)
    trainer_doc = db.collection("trainers").document(trainer)
    if not trainer_doc.get().exists:
        return (f"Trainer '{trainer}' not found.\n", 404)
    collection = trainer_doc.collection("pokemon")
    docs = [doc.to_dict() for doc in collection.get()]
    payload = {
        "name": trainer,
        "pokemon": docs
    }
    return (payload, 200)


@app.route("/trainers/<trainer>/pokemon", methods=["POST"])
def register_pokemon(trainer: str) -> tuple:
    """Register a pokemon for a trainer on Firestore."""
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        request_data = request.json
        if (
            request_data.get("id") is None or
            request_data.get("nickname") is None
        ):
            return ("Json body must contain the keys 'id' and 'nickname'.\n", 400)  # noqa: E501
        return _register_pokemon(trainer, request_data)
    else:
        return ("Content-Type is not of type application/json", 400)


def _register_pokemon(trainer: str, pokemon: dict) -> tuple:
    db = firestore.client(firestore_app)
    info = get_pokemon(pokemon["id"])
    trainer_doc = db.collection("trainers").document(trainer)
    pokemon_doc = trainer_doc.collection("pokemon").document(info["name"])
    data = {
        "id": pokemon["id"],
        "name": info["name"],
        "nickname": pokemon["nickname"],
        "level": 1,
        "caught_at": datetime.now(),
        "artwork": info["artwork"]
    }
    pokemon_doc.set(data)
    return ("Pokemon registered successfully.\n", 200)


@app.route("/trainers/<trainer>/pokemon/<pokemon>/level", methods=["POST"])
def level_up_pokemon(trainer: str, pokemon: str) -> tuple:
    """Level up a trainer's pokemon on Firestore."""
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        request_data = request.json
        if type(request_data.get("levels")) not in [int, type(None)]:
            return ("'levels' key must be an integer", 400)
        levels = request_data.get("levels", 1)
        return _level_up_pokemon(trainer, pokemon, levels)
    else:
        return ("Content-Type is not of type application/json", 400)


def _level_up_pokemon(trainer: str, pokemon: str, levels: int) -> tuple:
    db = firestore.client(firestore_app)
    trainer_doc = db.collection("trainers").document(trainer)
    if not trainer_doc.get().exists:
        return (f"Trainer '{trainer}' not registered", 404)
    pokemon_doc = trainer_doc.collection("pokemon").document(pokemon)
    if not pokemon_doc.get().exists:
        return (
            f"Pokemon '{trainer}' not registered for trainer '{trainer}'.\n",
            404
        )
    data = pokemon_doc.get().to_dict()
    data["level"] = data["level"] + levels
    pokemon_doc.set(data)
    return (data, 200)


if __name__ == "__main__":
    app.run(port="8080", debug=True)
