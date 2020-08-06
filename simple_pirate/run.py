"""
Reuses the server from Lazy Pirate
Adds a worker pool with load balancing
"""
import multiprocessing as mp
import sys
import time

from utils.logger import log
from simple_pirate.worker import worker
from simple_pirate.queue import queue
from lazy_pirate.client import request, ConnectionError


def make_requests():
    for i in range(1, 100):
        try:
            request(i)
        except ConnectionError as err:
            log.error(err)
            sys.exit(1)


if __name__ == '__main__':
    # Start the queue
    mp.Process(target=queue, daemon=True).start()
    # Start three workers
    mp.Process(target=worker, daemon=True).start()
    mp.Process(target=worker, daemon=True).start()
    mp.Process(target=worker, daemon=True).start()
    # Make requests
    mp.Process(target=make_requests, daemon=True).start()
    while True:
        time.sleep(1)
