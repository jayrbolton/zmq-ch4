# Paranoid Pirate Pattern

Extends the Simple Pirate pattern, adding worker heartbeating. The queue sends
heartbeat signals to the workers, and the workers send signals back to the
queue. When a worker fails, the queue re-sends the message to the next worker.

* Robust in the face of worker crash
* Does not restart workers; if all workers die, system is down
* Whole system crashes if the queue crashes

The client module from `lazy_pirate` is reused here.

* [queue](./queue.py)
* [worker](./worker.py)
* [run](./run.py) initialization and execution of the modules

Run from root with `poetry run python -m paranoid_pirate.run`
