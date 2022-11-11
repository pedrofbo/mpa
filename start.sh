COMPOSE_FILES="-f api/docker-compose.yml -f kafka/docker-compose.yml -f prometheus/docker-compose.yml"

docker-compose $COMPOSE_FILES down
docker-compose $COMPOSE_FILES up -d --build
sleep 15

for topic in $(cat ./topics.txt); do
    docker exec broker kafka-topics --bootstrap-server broker:9092 --create --topic $topic
done
