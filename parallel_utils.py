import threading
import time
from typing import Callable, Tuple
from utils import _logger
THREADS_LIST = []
MAX_NUM_THREADS = 40
MAX_WAIT_TIME_SECS = 120  # 2 min


def open_thread(target: Callable, args: Tuple = (), name=None) -> None:
    if name:
        t = threading.Thread(target=target, args=args, name=name)
    else:
        t = threading.Thread(target=target, args=args)
    t.start()
    THREADS_LIST.append(t)
    while len(THREADS_LIST) >= MAX_NUM_THREADS:
        thread = THREADS_LIST[0]
        thread.join()
        THREADS_LIST.pop(0)


def count_open_threads(name_prefix="") -> int:
    cnt = 0
    for thread in THREADS_LIST:
        cnt += name_prefix in thread.getName()
    return cnt


def wait_threads_to_finish(name_prefix="", limit=0):
    t_start = time.time()
    while count_open_threads("get_current_city_boards") < limit:
        t_curr = time.time()
        if t_curr - t_start > MAX_WAIT_TIME_SECS:
            _logger.error("TIMEOUT for threads of function: {}".format(name_prefix))
            break
