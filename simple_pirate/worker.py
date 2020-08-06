"""
Reuses the server from Lazy Pirate
Adds a worker pool with load balancing
"""
import time
import uuid
import zmq

from utils.print_seq import seqlog
from utils.logger import log

LRU_READY = "\x01"
WORKER_ADDR = "tcp://localhost:5556"


def worker():
    context = zmq.Context(1)
    worker = context.socket(zmq.REQ)
    identity = str(uuid.uuid4())
    worker.setsockopt_string(zmq.IDENTITY, identity)
    worker.connect(WORKER_ADDR)
    log.info(f"({identity}) worker ready")
    worker.send_string(LRU_READY)
    request_count = 0
    while True:
        msg = worker.recv_multipart()
        seqlog(['Queue', 'Worker'], msg[-1])
        if request_count == 1:
            log.info(f"({identity}) simulating CPU overload")
            time.sleep(3)
        elif request_count == 7:
            log.info(f"({identity}) simulating a crash")
            raise RuntimeError()
        else:
            log.info(f"({identity}) normal reply")
        time.sleep(0.5)  # Do some heavy work
        worker.send_multipart(msg)
        request_count += 1
