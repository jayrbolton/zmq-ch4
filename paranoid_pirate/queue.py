"""
Paranoid Pirate queue
"""
from collections import OrderedDict
import time
import zmq

from utils.print_seq import seqlog
from utils.logger import log
from paranoid_pirate.config import (
    HEARTBEAT_LIVENESS,
    HEARTBEAT_INTERVAL,
    CLIENT_ADDR,
    WORKER_ADDR,
    PPP_READY,
    PPP_HEARTBEAT,
)

# If a worker does not respond in HEARTBEAT_LIVENESS * HEARTBEAT_INTERVAL
# seconds, then it is dead


class Worker:
    """Small data structure representing a worker"""
    def __init__(self, address):
        self.address = address
        # TODO not sure
        self.expiry = time.time() + HEARTBEAT_INTERVAL * HEARTBEAT_LIVENESS


class WorkerQueue:
    def __init__(self):
        self.queue = OrderedDict()

    def ready(self, worker):
        self.queue[worker.address] = worker

    def purge(self):
        """Look for & kill expired workers."""
        t = time.time()
        for address, worker in self.queue.items():
            if t > worker.expiry:  # Worker expired
                self.queue.pop(address, None)

    def next(self):
        # Pop the next worker from the queue
        address, worker = self.queue.popitem()
        return address


def queue():
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)  # Clients
    backend = context.socket(zmq.ROUTER)  # Workers
    frontend.bind(CLIENT_ADDR)  # Clients
    backend.bind(WORKER_ADDR)  # Workers
    # Check for messages from the workers only
    poll_workers = zmq.Poller()
    poll_workers.register(backend, zmq.POLLIN)
    # Check for messages both from the client and workers
    poll_both = zmq.Poller()
    poll_both.register(frontend, zmq.POLLIN)
    poll_both.register(backend, zmq.POLLIN)
    workers = WorkerQueue()
    # Time of next heartbeat to send
    heartbeat_at = time.time() + HEARTBEAT_INTERVAL
    while True:
        if len(workers.queue) > 0:
            # We have active workers
            poller = poll_both
        else:
            # We have no active workers
            # TODO why don't we poll the client only?
            poller = poll_workers
        # Poll with a timeout of HEARTBEAT_INTERVAL seconds
        socks = dict(poller.poll(HEARTBEAT_INTERVAL * 1000))
        # Handle worker activity on backend if our sockets include the backend
        # socket
        if socks.get(backend) == zmq.POLLIN:
            # New message from the backend
            # Use worker address for LRU routing
            frames = backend.recv_multipart()
            if not frames:
                break
            address = frames[0]
            # Add the worker to the queue, with the key being its address
            # This will overwrite any existing workers, but with a new expiry
            workers.ready(Worker(address))
            # Validate control message, or return reply to client
            msg = frames[1:]
            if len(msg) == 1:
                # A message of length 1 must be a control signal
                if msg[0] not in (PPP_READY, PPP_HEARTBEAT):
                    log.error(f"Invalid message from worker: {msg}")
                signal = 'READY' if msg[0] == PPP_READY else 'HEARTBEAT'
                seqlog(['queue', 'worker'], signal, True)
            else:
                # Otherwise, it is a response from the worker to send back to
                # the client
                seqlog(['queue', 'worker'], msg[-1], rtl=True)
                log.info('[queue] sending response to client')
                frontend.send_multipart(msg)
            # Send heartbeats to idle workers if it's time
            if time.time() >= heartbeat_at:
                for worker in workers.queue:
                    # Send a multipart message, where the first part is the
                    # worker address, and the second part is the heartbeat
                    # control signal
                    msg = [worker, PPP_HEARTBEAT]
                    backend.send_multipart(msg)
                # Now that the heartbeat is sent, we can reset it to a time in
                # the future
                heartbeat_at = time.time() + HEARTBEAT_INTERVAL
        if socks.get(frontend) == zmq.POLLIN:
            # New message from the frontend
            frames = frontend.recv_multipart()
            if not frames:
                break
            seqlog(['client', 'queue'], frames[-1])
            # Pop a worker from the queue and insert its address in the first
            # part of the message
            frames.insert(0, workers.next())
            # Send the message to the workers with the inserted address
            backend.send_multipart(frames)
        # Remove any workers from the queue that have not responded to the
        # heartbeat, so are assumed dead
        workers.purge()
