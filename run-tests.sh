docker rm --force hexagonal_db_1
ENV=testing docker-compose -f docker-compose.yml -f tests/docker-compose.override.yml up
docker rm --force hexagonal_db_1
