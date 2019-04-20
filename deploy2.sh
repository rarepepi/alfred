$version_number = "v1.2"

docker build -t billbezo2929/alfred:{$version_number} .
docker push billbezo2929/alfred:{$version_number} .


# login to server



# cd into alfred


docker pull billbezo2929/alfred:{$version_number} . 