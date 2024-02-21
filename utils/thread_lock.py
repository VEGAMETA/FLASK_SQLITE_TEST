import time
import threading

lock = threading.Lock()


def locking(func):
    """
    Thread locking decorator
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        acquire = lock.acquire(blocking=False)
        while not acquire:
            acquire = lock.acquire(blocking=False)
            time.sleep(0.001)
        result = func(*args, **kwargs)
        lock.release()
        return result

    return wrapper
