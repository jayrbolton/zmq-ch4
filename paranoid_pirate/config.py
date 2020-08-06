
# How many tries when heartbeating a worker before assuming it is dead
HEARTBEAT_LIVENESS = 3     # 3..5 is reasonable
# How many tries when heartbeating a worker before assuming it is dead
# How often we heartbeat a worker
HEARTBEAT_INTERVAL = 1   # Seconds

# When the worker tries to reconnect, this is the maximum interval time (in
# seconds) that it will wait before retrying
INTERVAL_MAX = 32
# Time in seconds that we use as the interval for the worker to retry
# connecting to the queue. The retry interval increases from here up to
# INTERVAL_MAX
INTERVAL_INIT = 1

# Frontend socket address (between client and queue)
CLIENT_ADDR = "tcp://*:5555"
# Backend socket address (between queue and workers)
WORKER_ADDR = "tcp://*:5556"
WORKER_ADDR_FULL = "tcp://localhost:5556"

# Code that worker sends on boot to the queue that signals it is ready
PPP_READY = b"\x01"      # Signals worker is ready
# Code that the worker sends to the queue every HEARTBEAT_INTERVAL indicating
# it is still alive
PPP_HEARTBEAT = b"\x02"  # Signals worker heartbeat
