# Reliable Request-Reply Patterns

Refactored Python code examples with comments based on the various patterns from the [ZeroMQ guide, chapter 4](http://zguide.zeromq.org/php:chapter4).

The patterns:

* [Lazy Pirate Pattern](/lazy_pirate): reliable request-reply from the client side
* [Simple Pirate Pattern](./simple_pirate): reliable request-reply using with multiple workers and load balancing
* [Paranoid Pirate Pattern](./paranoid_pirate): reliable request-reply with heartbeating of the workers

TODO:

* [Majordomo](./majordomo): service-oriented reliable queueing
* [Titanic Pattern](titanic): disk-based/disconnected reliable queueing
* [Binary Star Pattern](binary-star): primary-backup server failover
* [Freelance Pattern](freelance): brokerless reliable request-reply

Set up dependencies with `pip install poetry && poetry install`.

Run any example with:

```py
poetry run python -m <directory>.run.py
```

See the corresponding `README.md` files in each subdirectory.

From the docs:

> Of all the different patterns, the two that stand out for production use are the Majordomo pattern, for broker-based reliability, and the Freelance pattern, for brokerless reliability.
