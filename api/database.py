from datetime import datetime

import firebase_admin
import requests
from firebase_admin import firestore
from google.cloud.firestore_v1.base_document import DocumentSnapshot

import models

firestore_app = firebase_admin.initialize_app(
    options={"projectId": "hotaru-gcp"}
)
db = firestore.client(firestore_app)


def get_pokemon(number: int) -> models.Pokemon:
    """Retrieve info on the PokeAPI, given a pokemon ID number."""
    url = f"https://pokeapi.co/api/v2/pokemon/{number}"
    response = requests.get(url).json()
    pokemon = models.Pokemon(
        id=response["id"],
        name=response["name"],
        artwork=response["sprites"]["other"]["official-artwork"]["front_default"]  # noqa: E501
    )
    return pokemon


def get_trainer_document(trainer: str) -> DocumentSnapshot:
    return db.collection("trainers").document(trainer)


def get_trainer(trainer: str) -> models.Trainer:
    doc = get_trainer_document(trainer)
    if doc.get().exists:
        trainer_data = models.Trainer.parse_obj(doc.get().to_dict())
        return trainer_data
    else:
        raise ValueError(f"Trainer '{trainer}' not found.")


def register_trainer(name: str, image: str) -> models.Trainer:
    doc = get_trainer_document(name)
    if not doc.get().exists:
        data = {
            "name": name,
            "image": image,
            "registered_at": datetime.now()
        }
        doc.set(data)
        trainer_data = models.Trainer.parse_obj(data)
        return trainer_data
    else:
        raise ValueError(f"Trainer '{name}' already registered.")


def get_trainer_pokemon(trainer: str) -> models.TrainerPokemon:
    trainer_doc = get_trainer_document(trainer)
    if trainer_doc.get().exists:
        collection = trainer_doc.collection("pokemon")
        docs = [doc.to_dict() for doc in collection.get()]
        data = {
            "name": trainer,
            "pokemon": docs
        }
        pokemon_data = models.TrainerPokemon.parse_obj(data)
        return pokemon_data
    else:
        raise ValueError(f"Trainer '{trainer}' not found.")


def register_pokemon(trainer: str, pokemon: models.RegisterPokemon) -> models.CaughtPokemon:  # noqa: E501
    info: models.Pokemon = get_pokemon(pokemon.id)
    trainer_doc = get_trainer_document(trainer)
    if not trainer_doc.get().exists:
        raise ValueError(f"Trainer '{trainer}' not found.")
    pokemon_doc = trainer_doc.collection("pokemon").document(info.name)
    data = {
        "id": info.id,
        "name": info.name,
        "nickname": pokemon.nickname,
        "level": pokemon.level,
        "caught_at": datetime.now(),
        "artwork": info.artwork
    }
    pokemon_doc.set(data)
    pokemon_data = models.CaughtPokemon.parse_obj(data)
    return pokemon_data


def level_up_pokemon(trainer: str, pokemon: str,
                     levels: int) -> models.CaughtPokemon:
    trainer_doc = get_trainer_document(trainer)
    if not trainer_doc.get().exists:
        raise ValueError(f"Trainer '{trainer}' not found.")
    pokemon_doc = trainer_doc.collection("pokemon").document(pokemon)
    if not pokemon_doc.get().exists:
        raise ValueError(
            f"Pokemon '{trainer}' not registered for trainer '{trainer}'.",
        )
    data = pokemon_doc.get().to_dict()
    data["level"] = data["level"] + levels
    pokemon_doc.set(data)
    pokemon_data = models.CaughtPokemon.parse_obj(data)
    return pokemon_data
