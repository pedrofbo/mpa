import random
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import database as db
import models
from kafka import kafka_logging

app = FastAPI()


@app.get("/pokemon/random", response_model=models.Pokemon)
@kafka_logging("POKEMON__RANDOM")
async def get_random_pokemon() -> JSONResponse:
    """Retrieve info for a random pokemon."""
    number = random.randrange(1, 906)
    pokemon: models.Pokemon = db.get_pokemon(number)
    return JSONResponse(pokemon.dict())


@app.get("/pokemon/{number}", response_model=models.Pokemon)
@kafka_logging("POKEMON__ID")
async def get_pokemon_from_number(number: int) -> JSONResponse:
    """Given a Pokemon ID, retrieve info about it.

    Parameters
    ----------
    number : int
        ID of the pokemon to retrieve.

    Returns
    -------
    JSONResponse
        Information about the fetched pokemon.
    """
    try:
        pokemon: models.Pokemon = db.get_pokemon(number)
        return JSONResponse(pokemon.dict())
    except Exception as e:
        return _handle_error(e)


@app.get("/trainers/{trainer}", response_model=models.Trainer)
@kafka_logging("TRAINERS__NAME")
async def get_trainer(trainer: str) -> JSONResponse:
    """Retrieve info on Firestore for a given trainer.

    Parameters
    ----------
    trainer : str
        Name of the trainer.

    Returns
    -------
    JSONResponse
        Information about the fetched trainer.
    """
    try:
        trainer_data: models.Trainer = db.get_trainer(trainer)
        json_data: dict = jsonable_encoder(trainer_data)
        return JSONResponse(json_data)
    except Exception as e:
        return _handle_error(e)


@app.post("/trainers", response_model=models.Trainer)
@kafka_logging("TRAINERS__REGISTER", "POST")
async def register_trainer(trainer: models.Trainer) -> JSONResponse:
    """Register given trainer.

    Parameters
    ----------
    trainer : models.Trainer
        Name of the trainer.

    Returns
    -------
    JSONResponse
        Information about the registered trainer.
    """
    try:
        trainer_data = db.register_trainer(trainer.name, trainer.image)
        json_data: dict = jsonable_encoder(trainer_data)
        return JSONResponse(json_data, 201)
    except Exception as e:
        return _handle_error(e)


@app.get("/trainers/{trainer}/pokemon", response_model=models.TrainerPokemon)
@kafka_logging("TRAINERS__NAME__POKEMON")
async def get_trainer_pokemon(trainer: str) -> JSONResponse:
    """Retrieve a list of pokemon for a given trainer.

    Parameters
    ----------
    trainer : str
        Name of the trainer.

    Returns
    -------
    JSONResponse
        List of registered pokemon for the given trainer.
    """
    try:
        pokemon_data: models.TrainerPokemon = db.get_trainer_pokemon(trainer)
        json_data: dict = jsonable_encoder(pokemon_data)
        return JSONResponse(json_data, 200)
    except Exception as e:
        return _handle_error(e)


@app.post("/trainers/{trainer}/pokemon", response_model=models.CaughtPokemon)
@kafka_logging("TRAINERS__NAME__POKEMON__REGISTER", "POST")
async def register_pokemon(trainer: str,
                           pokemon: models.RegisterPokemon) -> JSONResponse:
    """Register a pokemon for a given trainer.

    Parameters
    ----------
    trainer : str
        Name of the trainer.
    pokemon : models.RegisterPokemon
        Information about the pokemon to register.

    Returns
    -------
    JSONResponse
        Information about the registered pokemon.
    """
    try:
        pokemon_data: models.CaughtPokemon = db.register_pokemon(
            trainer, pokemon)
        json_data: dict = jsonable_encoder(pokemon_data)
        return JSONResponse(json_data, 201)
    except Exception as e:
        return _handle_error(e)


@app.post(
    "/trainers/{trainer}/pokemon/{pokemon}/level",
    response_model=models.RegisterPokemonResponse
)
@kafka_logging("TRAINERS__NAME__POKEMON__NAME__LEVEL__REGISTER", "POST")
async def level_up_pokemon(trainer: str, pokemon: str,
                           levels: models.Level) -> JSONResponse:
    """Raise the level of a trainer's pokemon..

    Parameters
    ----------
    trainer : str
        Name of the trainer.
    pokemon : str
        Name of the pokemon.
    levels : models.Level
        Number of levels to raise.

    Returns
    -------
    JSONResponse
        Information about the pokemon.
    """
    try:
        pokemon_data: models.RegisterPokemonResponse = db.level_up_pokemon(
            trainer, pokemon, levels.levels)
        json_data: dict = jsonable_encoder(pokemon_data)
        return JSONResponse(json_data, 201)
    except Exception as e:
        return _handle_error(e)


def _handle_error(error: Exception) -> JSONResponse:
    error_response = {
        "error_type": type(error).__name__,
        "error_message": str(error)
    }
    return JSONResponse(error_response, 404)


if __name__ == '__main__':
    uvicorn.run('server:app', host='0.0.0.0', port=8080)
