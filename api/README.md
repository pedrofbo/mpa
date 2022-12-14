# MPA API

Backend API to return and register information about trainers and their pokémon.
Developed with [FastAPI](https://fastapi.tiangolo.com/).

## Getting Started

A prerequirement to use this project is to have access to a [GCP](https://cloud.google.com/)
account and a project with the [Firestore](https://cloud.google.com/firestore) API enabled.

In order to run the API, you must have either:
- GCP credentials setup in your machine with read and write access to Firestore.
- A `serviceAccountKey.json` file with credentials to read and write on Firestore
(mandatory when running with docker).

Also, you must override the `project_id` constant in the `database.py` module to
match your project.

### Running locally

Setup a virtual environment and install the packages in `requirements.txt`.

```bash
python3 -m virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

Start the server on port 8080 by running:

```bash
python server.py
```

### Running with Docker

```bash
docker build -t mpa_api .
docker run --rm -p 8080:8080 -v ./serviceAccountKey.json:./serviceAccountKey.json -d mpa_api
```

Alternatively, run with `docker-compose`:

```bash
docker-compose up -d
```

## API endpoints

For an interactive and reader friendly documentation about the available endpoints,
check the `/docs` endpoint after starting the server. It is automatically generated
by FastAPI.
