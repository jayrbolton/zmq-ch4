# Simple Pirate Pattern

Extends the Lazy Pirate pattern to add multiple backend workers with load
balancing, while retaining the retry functionality on the client.

We use the LRU (least recently used) queue in-between the client and workers.

Notes:
* When the client times out, but the worker later gives the response to the
  queue, then it is discarded.

In this scheme, workers that crash don't get automatically restarted. See the next section, `paranoid_pirate`, for worker heartbeats and restarting.

The client module from `lazy_pirate` is reused here.

* [queue](./queue.py)
* [worker](./worker.py)
* [run](./run.py) initialization and execution of the modules

Run from root with `poetry run python -m simple_pirate.run`
