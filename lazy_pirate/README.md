# The Lazy Pirate Pattern

In a request-reply (client/server) setup, this pattern prevents the client from hanging indefinitely by implementing request retries.

This pattern is not able to redirect requests to alternate servers on failure.

* [server](./server.py)
* [client](./client.py)
