import sys

from concurrent.futures import ThreadPoolExecutor
from celery_race_condition.tasks import add

POOL = ThreadPoolExecutor(100)

def call_and_retrieve(a, b):
    async_result = add.delay(a, b)
    async_result.wait(timeout=100, propagate=True)
    return async_result.get()

if __name__ == "__main__":
    num_calls = int(sys.argv[1])
    futures = ([
        POOL.submit(call_and_retrieve, a, a)
        for a in range(num_calls)
    ])

    for future in futures:
        future.result()