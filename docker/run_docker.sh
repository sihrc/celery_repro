#! /bin/bash
docker build -t celery_race_condition .
docker stop celery_race_condition
docker rm celery_race_condition
docker run -v $(pwd):/celery_race_condition --name {[package}} -dt celery_race_condition bash
docker exec -it celery_race_condition bash
