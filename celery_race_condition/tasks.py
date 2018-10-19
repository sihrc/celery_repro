from celery_race_condition.celery_app import CELERY_APP

@CELERY_APP.task
def add(a, b):
    return a + b