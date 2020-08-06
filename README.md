
# Reliable Request-Reply Patterns

Python code examples with annotation from the [ZeroMQ guide, chapter 4](http://zguide.zeromq.org/php:chapter4).

* [lazy_pirate](/lazy_pirate): reliable request-reply from the client side
* [simple_pirate](./simple_pirate): reliable request-reply using load balancing
* [paranoid_pirate](./paranoid_pirate): reliable request-reply with heartbeating

Set up dependencies with `pip install poetry && poetry install`.

Run any example with:

```py
PYTHONPATH=. poetry run python <directory>/run.py
```

From the source:

> Of all the different patterns, the two that stand out for production use are the Majordomo pattern, for broker-based reliability, and the Freelance pattern, for brokerless reliability.
