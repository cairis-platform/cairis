# INSTRUCTION TO BUILD AND BRING UP SETUP WITH DOCKER

## 1. Build docker image

By default, the cairis backend source code is fetched from github repo. The below script will help to build docker image locally.
You can specify the image version. By default, it is "latest".

```sh
./buildLocalImage.sh
```

## 2. Startup servers

Foreground mode (to exit, press CTRL + C):

```sh
docker compose up
```

Background mode:

```sh
docker compose up -d
```

To stop the servers:

```sh
docker compose down
```

## 3. Create a user

"cairis-CAIRIS-1" is the name of docker container of the cairis server.

```sh
docker exec -t cairis-CAIRIS-1 ./addAccount.sh test@test.com test TestUser
```
