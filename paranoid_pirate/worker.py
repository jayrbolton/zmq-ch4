"""
Paranoid Pirate worker
"""
from random import randint
from uuid import uuid4
import time
import zmq

from utils.logger import log
from utils.print_seq import seqlog
from paranoid_pirate.config import (
    HEARTBEAT_LIVENESS,
    HEARTBEAT_INTERVAL,
    INTERVAL_MAX,
    INTERVAL_INIT,
    WORKER_ADDR_FULL,
    PPP_READY,
    PPP_HEARTBEAT,
)


def init_worker_socket(context, poller):
    """Helper function that returns a new configured socket
       connected to the Paranoid Pirate queue"""
    worker = context.socket(zmq.DEALER)  # Socket connecting to the queue
    identity = str(uuid4()).encode()
    worker.setsockopt(zmq.IDENTITY, identity)
    poller.register(worker, zmq.POLLIN)
    worker.connect(WORKER_ADDR_FULL)
    worker.send(PPP_READY)
    return worker


def worker():
    context = zmq.Context(1)
    poller = zmq.Poller()
    # Counter of how many times a heartbeat has failed
    liveness = HEARTBEAT_LIVENESS
    # Starting value for the retry interval time
    interval = INTERVAL_INIT
    # When to initially send a heartbeat signal
    heartbeat_at = time.time() + HEARTBEAT_INTERVAL
    worker = init_worker_socket(context, poller)
    # How many requests we have processed
    cycles = 0
    while True:
        # Wait for messages from the queue with a timeout of HEARTBEAT_INTERVAL
        # seconds
        socks = dict(poller.poll(HEARTBEAT_INTERVAL * 1000))
        # Handle worker activity on backend
        if socks.get(worker) == zmq.POLLIN:
            #  Received a message from the queue that is either:
            #    Request: 3-part envelope + content
            #    Heartbeat: 1-part HEARTBEAT
            frames = worker.recv_multipart()
            if not frames:
                break  # Interrupted
            if len(frames) == 3:
                seqlog(['queue', 'worker'], frames[-1])
                # Simulate various problems, after a few cycles
                cycles += 1
                if cycles > 3 and randint(0, 5) == 0:
                    log.info("[worker] Worker simulating a crash")
                    break
                if cycles > 3 and randint(0, 5) == 0:
                    log.info("[worker] Simulating CPU overload")
                    time.sleep(3)
                log.info("[worker] Normal reply")
                # Echo back the request as the response
                worker.send_multipart(frames)
                # Reset heartbeat failure counter
                liveness = HEARTBEAT_LIVENESS
                time.sleep(1)  # Do some heavy work
            elif len(frames) == 1 and frames[0] == PPP_HEARTBEAT:
                seqlog(['queue', 'worker'], 'HEARTBEAT')
                liveness = HEARTBEAT_LIVENESS
            else:
                log.error(f"[worker] Invalid message: {frames}")
            interval = INTERVAL_INIT
        else:
            # No message from the queue; we timed out, but were expecting at
            # least a heartbeat
            liveness -= 1
            if liveness == 0:
                log.error("Heartbeat failure, can't reach queue")
                log.info(f"Reconnecting in {interval}")
                time.sleep(interval)
                if interval < INTERVAL_MAX:
                    # Double the retry interval if it is below the max
                    interval *= 2
                poller.unregister(worker)
                # Discard any pending messages from the socket
                worker.setsockopt(zmq.LINGER, 0)
                worker.close()
                # Try to reconnect and reinitialize
                worker = init_worker_socket(context, poller)
                liveness = HEARTBEAT_LIVENESS
        if time.time() > heartbeat_at:
            # Send a heartbeat from the worker to the queue
            heartbeat_at = time.time() + HEARTBEAT_INTERVAL
            worker.send(PPP_HEARTBEAT)
