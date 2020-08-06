"""
Lazy pirate client
Author: Daniel Lundin <dln(at)eintr(dot)org>
"""
import sys
import zmq

from utils.print_seq import seqlog
from utils.logger import log

REQUEST_TIMEOUT = 1000
REQUEST_RETRIES = 6
SERVER_ENDPOINT = "tcp://localhost:5555"


def request(content):
    """
    Make a request to a server with retries on failure
    """
    context = zmq.Context()
    client = context.socket(zmq.REQ)
    client.connect(SERVER_ENDPOINT)
    request = str(content).encode()
    client.send(request)
    retries_left = REQUEST_RETRIES
    while True:
        if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            reply = client.recv_multipart()
            seqlog(['client', 'queue'], payload=reply[-1], rtl=True)
            return reply
        retries_left -= 1
        if retries_left == 0:
            context.destroy(linger=0)
            client.close()
            raise ConnectionError("[client] Unable to reach the server")
        log.warning("[client] No response from server")
        # Socket is confused. Close and remove it.
        client.setsockopt(zmq.LINGER, 0)
        client.close()
        log.warning("[client] Reconnecting to server…")
        # Create new connection
        client = context.socket(zmq.REQ)
        client.connect(SERVER_ENDPOINT)
        log.warning(f"[client] Resending ({request})")
        client.send(request)


class ConnectionError(Exception):
    pass


if __name__ == '__main__':
    for i in range(1, 10):
        try:
            request(i)
        except ConnectionError as err:
            log.error('[client] ' + str(err))
            sys.exit(1)
