import threading
import os
import uuid
from importlib import import_module

import msgpack

import celery
from celery.backends.redis import RedisBackend
from celery.concurrency import asynpool
from celery.result import allow_join_result
from kombu.serialization import register

CELERY_TASK_TIMEOUT = 10
asynpool.PROC_ALIVE_TIMEOUT = 600
API_TASK_NAME_FORMAT = "{api_name}_{queue}_{method_name}"

from celery.backends.redis import RedisBackend

local_context = threading.local()
class Backend(RedisBackend):
    @property
    def result_consumer(self):
        consumer = getattr(local_context, "consumer", None)
        if consumer:
            return consumer

        local_context.consumer = self.ResultConsumer(
            self, self.app, self.accept,
            self._pending_results, self._pending_messages,
        )

        return local_context.consumer

    @result_consumer.setter
    def result_consumer(self, value):
        local_context.consumer = value

def DEFAULT_QUEUE_NAME_FORMAT(api_name, queue): return "{api_name}_{queue}".format(
    api_name=api_name,
    queue=queue
)

def unpackb(*args, **kwargs):
    kwargs["encoding"] = "latin-1"
    return msgpack.unpackb(*args, **kwargs)


def packb(*args, **kwargs):
    kwargs["use_bin_type"] = True
    return msgpack.packb(*args, **kwargs)


CELERY_APP = celery.Celery(
    "indicoapi",
    broker="amqp://user:password@rabbitmq:5672"
)

CELERY_APP.conf.update(
    task_serializer="msgpack",
    result_serializer="msgpack",
    result_expires=60 * 60 * 24,
    task_always_eager=False,
    accept_content=["application/x-msgpack"],
    result_backend=__name__ + ".Backend",
    redis_port="6379",
    redis_host="redis",
    broker_transport_options={
        "confirm_publish": True
    },
    broker_heartbeat=20,
    broker_connection_max_retries=None,
    task_queue_ha_policy="all"
)