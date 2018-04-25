docker rm --force hexagonal_db_1
ENV=testing docker-compose -f docker-compose.yml -f tests/docker-compose.override.yml up --abort-on-container-exit
docker rm --force hexagonal_db_1
