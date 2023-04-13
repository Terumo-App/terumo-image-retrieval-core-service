pipenv requirements > requirements.txt
docker build -t terumo-image-retrieval-core-service .

docker tag terumo-image-retrieval-core-service terumoapp/terumo-image-retrieval-core-service:latest
