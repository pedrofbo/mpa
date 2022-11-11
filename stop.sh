COMPOSE_FILES="-f api/docker-compose.yml -f kafka/docker-compose.yml -f prometheus/docker-compose.yml"

docker-compose $COMPOSE_FILES down
