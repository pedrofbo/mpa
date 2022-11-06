docker-compose down
docker-compose up -d
sleep 10
docker exec broker kafka-topics --bootstrap-server broker:9092 --create --topic quickstart
