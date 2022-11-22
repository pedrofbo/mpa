from datetime import datetime
from typing import List

from pydantic import BaseModel


class Pokemon(BaseModel):
    id: int
    name: str
    artwork: str


class Trainer(BaseModel):
    name: str
    image: str
    registered_at: datetime = None


class CaughtPokemon(BaseModel):
    id: int
    name: str
    nickname: str
    level: int
    caught_at: datetime
    artwork: str


class TrainerPokemon(BaseModel):
    name: str
    pokemon: List[CaughtPokemon]


class RegisterPokemon(BaseModel):
    id: int
    nickname: str
    level: int = 1


class RegisterPokemonResponse(CaughtPokemon):
    trainer: str


class Level(BaseModel):
    levels: int = 1
