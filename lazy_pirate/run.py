import multiprocessing as mp
import sys

from lazy_pirate.client import request
from lazy_pirate.server import server
from utils.logger import log


if __name__ == '__main__':
    mp.Process(target=server, daemon=True).start()
    for i in range(1, 10):
        try:
            request(i)
        except ConnectionError as err:
            log.error(err)
            sys.exit(1)
