# Reliable Request-Reply Patterns

Refactored Python code examples with large amounts of comments based on the various patterns from the [ZeroMQ guide, chapter 4](http://zguide.zeromq.org/php:chapter4).

Finished:

* [Lazy Pirate Pattern](/lazy_pirate): reliable request-reply from the client side
* [Simple Pirate Pattern](./simple_pirate): reliable request-reply using with multiple workers and load balancing
* [Paranoid Pirate Pattern](./paranoid_pirate): reliable request-reply with heartbeating of the workers

TODO:

* [Majordomo](http://zguide.zeromq.org/php:chapter4#Service-Oriented-Reliable-Queuing-Majordomo-Pattern)
* [Async Majordomo](http://zguide.zeromq.org/php:chapter4#Asynchronous-Majordomo-Pattern)
* [Service Discovery](http://zguide.zeromq.org/php:chapter4#Service-Discovery)
* [Titanic Pattern](http://zguide.zeromq.org/php:chapter4#Disconnected-Reliability-Titanic-Pattern)
* [Binary Star Pattern](http://zguide.zeromq.org/php:chapter4#High-Availability-Pair-Binary-Star-Pattern)
* [Freelance Pattern](http://zguide.zeromq.org/php:chapter4#Brokerless-Reliability-Freelance-Pattern)

Set up dependencies with `pip install poetry && poetry install`.

Run any example with:

```py
poetry run python -m <directory>.run.py
```

From the docs:

> Of all the different patterns, the two that stand out for production use are the Majordomo pattern, for broker-based reliability, and the Freelance pattern, for brokerless reliability.
