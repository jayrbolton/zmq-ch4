from utils.print_seq import seqlog
from utils.logger import log
import zmq

LRU_READY = "\x01"
WORKER_ADDR = "tcp://*:5556"
CLIENT_ADDR = "tcp://*:5555"


def queue():
    """
    Load balancer
    - takes requests from the client and sends them into the workers' socket
    - takes messages from the workers and forwards them back to the clients
    """
    context = zmq.Context(1)
    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.ROUTER)
    frontend.bind(CLIENT_ADDR)
    backend.bind(WORKER_ADDR)
    poll_workers = zmq.Poller()
    poll_workers.register(backend, zmq.POLLIN)
    poll_both = zmq.Poller()
    poll_both.register(frontend, zmq.POLLIN)
    poll_both.register(backend, zmq.POLLIN)
    workers = []
    log.info("Queue has started")
    while True:
        if len(workers) > 0:
            socks = dict(poll_both.poll())
        else:
            socks = dict(poll_workers.poll())
        if socks.get(backend) == zmq.POLLIN:
            # Handle worker activity on backend
            # Use worker address for LRU routing
            msg = backend.recv_multipart()
            if not msg:
                continue
            address = msg[0]
            workers.append(address)
            # Everything after the second (delimiter) frame is reply
            reply = msg[2:]
            # Forward message to client if it's not a READY
            if reply[0] != LRU_READY:
                seqlog(['Worker', 'Queue'], payload=reply[-1], rtl=False)
                frontend.send_multipart(reply)
        if socks.get(frontend) == zmq.POLLIN:
            # Get client request, route to first available worker
            msg = frontend.recv_multipart()
            request = [workers.pop(0), ''.encode()] + msg
            seqlog(['Client', 'Queue'], msg[-1])
            backend.send_multipart(request)


if __name__ == '__main__':
    pass
