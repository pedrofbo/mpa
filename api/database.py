import os
from datetime import datetime

import firebase_admin
import requests
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_document import DocumentSnapshot

import models

credentials_path = "serviceAccountKey.json"
if os.path.exists(credentials_path):
    credentials = credentials.Certificate(credentials_path)
    firestore_app = firebase_admin.initialize_app(
        credentials,
        options={"projectId": "hotaru-gcp"}
    )
else:
    firestore_app = firebase_admin.initialize_app(
        options={"projectId": "hotaru-gcp"}
    )
db = firestore.client(firestore_app)


def get_pokemon(number: int) -> models.Pokemon:
    """Retrieve info on the PokeAPI, given a pokemon ID number.

    Parameters
    ----------
    number : int
        ID of a pokemon.

    Returns
    -------
    models.Pokemon
        Information about the pokemon retrived from the PokeAPI.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{number}"
    response = requests.get(url).json()
    pokemon = models.Pokemon(
        id=response["id"],
        name=response["name"],
        artwork=response["sprites"]["other"]["official-artwork"]["front_default"]  # noqa: E501
    )
    return pokemon


def get_trainer_document(trainer: str) -> DocumentSnapshot:
    """Retrive document from Firestore with information about a trainer.

    Parameters
    ----------
    trainer : str
        Name of the trainer.

    Returns
    -------
    google.cloud.firestore_v1.base_document.DocumentSnapshot
        Snapshot of trainer document.
    """
    return db.collection("trainers").document(trainer)


def get_trainer(trainer: str) -> models.Trainer:
    """Retrieve information about a trainer from Firestore.

    Parameters
    ----------
    trainer : str
        Name of the trainer.

    Returns
    -------
    models.Trainer
        Trainer information.

    Raises
    ------
    ValueError
        Trainer not found on Firestore.
    """
    doc = get_trainer_document(trainer)
    if doc.get().exists:
        trainer_data = models.Trainer.parse_obj(doc.get().to_dict())
        return trainer_data
    else:
        raise ValueError(f"Trainer '{trainer}' not found.")


def register_trainer(name: str, image: str) -> models.Trainer:
    """Register a given trainer on Firestore.

    Parameters
    ----------
    name : str
        Name of the trainer.
    image : str
        Trainer's image.

    Returns
    -------
    models.Trainer
        Information about the registered trainer.

    Raises
    ------
    ValueError
        Trainer already registered on Firestore.
    """
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
    """Retrieve a list of pokemon from the given trainer on Firestore.

    Parameters
    ----------
    trainer : str
        Name of the trainer.

    Returns
    -------
    models.TrainerPokemon
        List of pokemon owned by the trainer.

    Raises
    ------
    ValueError
        Trainer not found on Firestore.
    """
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
    """Register a given pokemon to a given trainer on Firestore.

    Parameters
    ----------
    trainer : str
        Name of the trainer.
    pokemon : models.RegisterPokemon
        Information about the pokemon to be registered.

    Returns
    -------
    models.CaughtPokemon
        Information about the registered pokemon.

    Raises
    ------
    ValueError
        Trainer not found on Firestore.
    """
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
    """Raise the level of a given pokemon by a given amount of levels.

    Parameters
    ----------
    trainer : str
        Name of the trainer that the given pokemon is registered under.
    pokemon : str
        Name of the pokemon.
    levels : int
        Levels to be raised.

    Returns
    -------
    models.CaughtPokemon
        Information about the pokemon.

    Raises
    ------
    ValueError
        Trainer not found on Firestore.
    ValueError
        Pokemon not found on Firestore under the given trainer.
    """
    trainer_doc = get_trainer_document(trainer)
    if not trainer_doc.get().exists:
        raise ValueError(f"Trainer '{trainer}' not found.")
    pokemon_doc = trainer_doc.collection("pokemon").document(pokemon)
    if not pokemon_doc.get().exists:
        raise ValueError(
            f"Pokemon '{pokemon}' not registered for trainer '{trainer}'.",
        )
    data = pokemon_doc.get().to_dict()
    data["level"] = data["level"] + levels
    pokemon_doc.set(data)
    pokemon_data = models.CaughtPokemon.parse_obj(data)
    return pokemon_data
