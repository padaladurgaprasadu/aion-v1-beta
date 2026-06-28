import logging
import time
import functools
import json
import traceback

# Configure standard logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_logger(name: str):
    """Returns a configured logger instance."""
    return logging.getLogger(name)

def measure_time(logger=None):
    """
    A decorator that logs the execution time of a function.
    Useful for measuring agent response times.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log = logger or get_logger(func.__module__)
            start_time = time.perf_counter()
            log.info(f"Started executing '{func.__name__}'...")
            
            try:
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                elapsed = end_time - start_time
                log.info(f"[METRIC] '{func.__name__}' completed successfully in {elapsed:.2f} seconds.")
                return result
            except Exception as e:
                end_time = time.perf_counter()
                elapsed = end_time - start_time
                log.error(f"[METRIC] '{func.__name__}' failed after {elapsed:.2f} seconds.")
                log.error(f"Exception details:\n{traceback.format_exc()}")
                raise e
        return wrapper
    return decorator
