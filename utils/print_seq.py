from typing import List

from utils.logger import log


def seqlog(seq: List[str], payload=None, rtl=False):
    ret = ""
    if rtl:
        ret = ' ← '.join(seq)
    else:
        ret = ' → '.join(seq)
    if payload is not None:
        ret += f" [{payload}]"
    log.info(ret)
