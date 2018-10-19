# celery_race_condition
Reproducing race condition from celery redis backend

Built on: Python3 and Docker (alpine)<br>
Maintained by: Chris Lee [chris@indico.io]

## Getting Started
```bash
docker-compose up --build
```

```
docker exec -it celery_race_condition_app_1 bash
python3 -m celery_race_condition.app 5
python3 -m celery_race_condition.app 100
python3 -m celery_race_condition.app 1000 # Errors out on more
```
