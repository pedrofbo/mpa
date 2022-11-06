from typing import Union

import random
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse

import database as db
import models

app = FastAPI()


@app.get("/pokemon/random", response_model=models.Pokemon)
async def get_random_pokemon() -> JSONResponse:
    """Retrieve info for a random pokemon."""
    number = random.randrange(1, 906)
    pokemon: models.Pokemon = db.get_pokemon(number)
    return JSONResponse(pokemon.dict())


@app.get("/pokemon/{number}", response_model=models.Pokemon)
async def get_pokemon_from_number(number: int) -> JSONResponse:
    """Given a Pokemon ID, retrieve info about it."""
    pokemon: models.Pokemon = db.get_pokemon(number)
    return JSONResponse(pokemon.dict())


@app.get("/trainers/{trainer}", response_model=models.Trainer)
async def get_trainer(trainer: str) -> Union[JSONResponse, PlainTextResponse]:
    """Retrieve info on Firestore for a given trainer."""
    try:
        trainer_data: models.Trainer = db.get_trainer(trainer)
        json_data: dict = jsonable_encoder(trainer_data)
        return JSONResponse(json_data)
    except ValueError as e:
        return PlainTextResponse(str(e), 404)


@app.post("/trainers", response_model=models.Trainer)
async def register_trainer(trainer: models.Trainer) -> Union[JSONResponse, PlainTextResponse]:  # noqa: E501
    """Register given trainer on Firestore."""
    try:
        trainer_data = db.register_trainer(trainer.name, trainer.image)
        json_data: dict = jsonable_encoder(trainer_data)
        return JSONResponse(json_data, 201)
    except ValueError as e:
        return PlainTextResponse(str(e), 400)


@app.get("/trainers/{trainer}/pokemon", response_model=models.TrainerPokemon)
def get_trainer_pokemon(trainer: str) -> tuple:
    """Retrieve a list of pokemon on Firestore for a given trainer."""
    try:
        pokemon_data: models.TrainerPokemon = db.get_trainer_pokemon(trainer)
        json_data: dict = jsonable_encoder(pokemon_data)
        return JSONResponse(json_data, 200)
    except ValueError as e:
        return PlainTextResponse(str(e), 404)


@app.post("/trainers/{trainer}/pokemon", response_model=models.CaughtPokemon)
async def register_pokemon(
    trainer: str, pokemon: models.RegisterPokemon
) -> Union[JSONResponse, PlainTextResponse]:
    """Register a pokemon for a trainer on Firestore."""
    try:
        pokemon_data: models.CaughtPokemon = db.register_pokemon(
            trainer, pokemon)
        json_data: dict = jsonable_encoder(pokemon_data)
        return JSONResponse(json_data, 201)
    except ValueError as e:
        return PlainTextResponse(str(e), 400)


@app.post(
    "/trainers/{trainer}/pokemon/{pokemon}/level",
    response_model=models.CaughtPokemon
)
def level_up_pokemon(
    trainer: str, pokemon: str, levels: models.Level
) -> Union[JSONResponse, PlainTextResponse]:
    """Level up a trainer's pokemon on Firestore."""
    try:
        pokemon_data: models.CaughtPokemon = db.level_up_pokemon(
            trainer, pokemon, levels.levels)
        json_data: dict = jsonable_encoder(pokemon_data)
        return JSONResponse(json_data, 201)
    except ValueError as e:
        return PlainTextResponse(str(e), 400)


if __name__ == '__main__':
    uvicorn.run('server:app', host='0.0.0.0', port=8080)
