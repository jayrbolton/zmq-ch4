"""
Lazy Pirate server
Has the following behavior:
    - first request is successfully responded to
    - next request times out
    - next few request are okay again
    - last request crashes the server
"""
import logging
import time
import zmq

from utils.print_seq import seqlog

ADDR = "tcp://*:5555"


def server():
    context = zmq.Context()
    server = context.socket(zmq.REP)
    server.bind(ADDR)
    request_count = 0
    while True:
        logging.info("Waiting for a request")
        request = server.recv()
        seqlog(['Client', 'Queue'], payload=request)
        # Simulate various problems, after a few cycles
        if request_count == 1:
            logging.info("Simulating CPU overload")
            # Client request timeout must be <3s
            time.sleep(3)
        elif request_count == 6:
            logging.info("Simulating a crash")
            break
        logging.info(f"Normal request ({request})")
        time.sleep(0.5)  # Do some heavy work
        server.send(request)
        request_count += 1


if __name__ == '__main__':
    server()
