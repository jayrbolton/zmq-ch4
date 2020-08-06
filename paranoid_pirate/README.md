# Paranoid Pirate Pattern

Extends the Simple Pirate pattern, adding worker failover by regularly checking
on their status.

* Robust in the face of worker crash

The queue is still a bottleneck, and the whole system will crash if the queue crashes.

* [queue](./queue.py)
* [worker](./worker.py)
* [run](./run.py) initialization and execution of the modules

Run from root with `PYTHONPATH=. python simple_pirate/run.py`

