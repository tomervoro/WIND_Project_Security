import threading
import time
from typing import Callable, Tuple
from utils import _logger
THREADS_LIST = []
MAX_NUM_THREADS = 20
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


def wait_threads_to_finish(name_prefix=""):
    for indx, thread in enumerate(THREADS_LIST):
        if name_prefix in thread.getName():
            thread.join()
            THREADS_LIST.pop(indx)