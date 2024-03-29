import time
import functools

class Wrap:
    """I made this class to bundle up the output
    and the run time of the function ran in timeit into an object."""
    def __init__(self, result, runtime):
        self.result = result
        self.runtime = runtime

def timeit(func=None, ndigits=2, wrap=True):
    """Decorator function used to time the execution of functions."""
    if not func:
        return functools.partial(timeit, ndigits=ndigits)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        ret = func(*args, **kwargs)
        finish = time.perf_counter()
        runtime = round(finish - start, ndigits)
        if wrap:
            return Wrap(ret, runtime)
        else:
            print(f"{func.__name__} finished in {runtime} second(s)")
            return ret
    return wrapper