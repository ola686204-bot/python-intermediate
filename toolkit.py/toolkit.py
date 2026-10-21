""" ToolKit.py
    Reusable decorator library for python microservices."""

"""
toolkit.py

Reusable decorator library for Python microservices.
"""


import inspect
import time
from collections import OrderedDict
from functools import wraps

def timer(unit: str = "ms"):
    """
    Measure execution time of a function.

    Args:
        unit (str):
            Output unit:
            - 's'  : seconds
            - 'ms' : milliseconds
            - 'us' : microseconds

    Returns:
        callable:
            Decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()

            result = func(*args, **kwargs)

            elapsed = time.perf_counter() - start

            conversions = {
                "s": 1,
                "ms": 1000,
                "us": 1_000_000,
            }

            if unit not in conversions:
                raise ValueError(
                    "unit must be one of: 's', 'ms', 'us'"
                )

            value = elapsed * conversions[unit]

            print(
                f"[TIMER] {func.__name__} "
                f"completed in {value:.2f}{unit}"
            )

            return result

        return wrapper

    return decorator


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions=(Exception,),
):
    """
    Retry a function when specified exceptions occur.

    Args:
        max_attempts (int):
            Maximum number of attempts.

        delay (float):
            Delay in seconds between attempts.

        exceptions (tuple):
            Exceptions to catch.

    Returns:
        callable:
            Decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)

                except exceptions as exc:
                    last_error = exc

                    print(
                        f"[RETRY] Attempt "
                        f"{attempt}/{max_attempts} "
                        f"failed: {exc}"
                    )

                    if attempt < max_attempts:
                        time.sleep(delay)

            raise RuntimeError(
                f"'{func.__name__}' "
                f"failed after {max_attempts} attempts"
            ) from last_error

        return wrapper

    return decorator


def validate_types(func):
    """
    Validate function arguments using type annotations.

    Args:
        func (callable):
            Wrapped function.

    Returns:
        callable:
            Decorated function.

    Raises:
        TypeError:
            If an annotated argument receives
            an incompatible type.
    """

    signature = inspect.signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)

        annotations = func.__annotations__

        for arg_name, value in bound.arguments.items():

            if arg_name not in annotations:
                continue

            expected = annotations[arg_name]

            if not isinstance(value, expected):
                raise TypeError(
                    f"argument '{arg_name}' "
                    f"expected {expected.__name__}, "
                    f"got {type(value).__name__}"
                )

        return func(*args, **kwargs)

    return wrapper


def cache(maxsize: int = 128):
    """
    Custom LRU cache.

    Args:
        maxsize (int):
            Maximum cache size.

    Returns:
        callable:
            Decorated function.
    """

    def decorator(func):
        storage = OrderedDict()

        hits = 0
        misses = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal hits
            nonlocal misses

            key = (
                args,
                tuple(sorted(kwargs.items())),
            )

            if key in storage:
                hits += 1

                storage.move_to_end(key)

                return storage[key]

            misses += 1

            result = func(*args, **kwargs)

            storage[key] = result

            storage.move_to_end(key)

            if len(storage) > maxsize:
                storage.popitem(last=False)

            return result

        def cache_info():
            """
            Return cache statistics.
            """

            return {
                "hits": hits,
                "misses": misses,
                "maxsize": maxsize,
                "currsize": len(storage),
            }

        def cache_clear():
            """
            Clear cache and reset statistics.
            """
            nonlocal hits
            nonlocal misses

            storage.clear()

            hits = 0
            misses = 0

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear

        return wrapper

    return decorator


def require_auth(roles=("admin",)):
    """
    Role-based authorization decorator.

    Args:
        roles (tuple):
            Allowed roles.

    Returns:
        callable:
            Decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            user = kwargs.get("user")

            if user is None:
                raise ValueError(
                    "user argument is required"
                )

            role = user.get("role")

            if role not in roles:
                raise PermissionError(
                    f"User role '{role}' "
                    f"is not authorized. "
                    f"Required: {roles}"
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator
