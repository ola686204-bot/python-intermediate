
"""demo.py

Demonstrates all decorators from toolkit.py.

Run:
    python demo.py
"""

import time

from toolkit import (
    timer,
    retry,
    validate_types,
    cache,
    require_auth,
)


print("=" * 20)
print("TIMER DEMONSTRATIONS")
print("=" * 20)


@timer(unit="ms")
def fast_task():
    """Fast task."""
    time.sleep(0.01)


@timer(unit="s")
def slow_task():
    """Slow task."""
    time.sleep(1)


@timer(unit="us")
def micro_task():
    """Micro task."""
    return sum(range(10))


fast_task()
slow_task()
micro_task()

print()


print("=" * 20)
print("RETRY DEMONSTRATIONS")
print("=" * 20)


failure_counter = {"count": 0}


@retry(max_attempts=3, delay=0.5)
def unstable_service():
    """Fails once, then succeeds."""
    failure_counter["count"] += 1

    if failure_counter["count"] < 2:
        raise ConnectionError("temporary outage")

    return "service available"


try:
    result = unstable_service()
    print(f"SUCCESS: {result}")
except Exception as exc:
    print(exc)


@retry(max_attempts=3, delay=0.5)
def always_fail():
    """Always fails."""
    raise RuntimeError("database unavailable")


try:
    always_fail()
except Exception as exc:
    print(f"EXPECTED FAILURE: {exc}")

print()


print("=" * 20)
print("VALIDATE_TYPES DEMONSTRATIONS")
print("=" * 20)


@validate_types
def calculate_total(price: float, quantity: int):
    return price * quantity


try:
    total = calculate_total(9.99, 5)
    print(f"SUCCESS: total={total}")
except TypeError as exc:
    print(exc)


try:
    calculate_total("abc", 5)
except TypeError as exc:
    print(f"EXPECTED FAILURE: {exc}")


@validate_types
def no_annotations(a, b):
    return a + b


print(
    "NO ANNOTATION SUCCESS:",
    no_annotations("hello ", "world"),
)

print()


print("=" * 20)
print("CACHE DEMONSTRATIONS")
print("=" * 20)


@cache(maxsize=2)
def expensive_square(n):
    print(f"Computing square for {n}")
    return n * n


print(expensive_square(3))
print(expensive_square(3))
print(expensive_square(4))
print(expensive_square(5))

print("CACHE INFO:")
print(expensive_square.cache_info())

expensive_square.cache_clear()

print("CACHE CLEARED:")
print(expensive_square.cache_info())

print()


print("=" * 20)
print("REQUIRE_AUTH DEMONSTRATIONS")
print("=" * 20)


@require_auth(roles=("admin",))
def delete_user(user=None):
    return "user deleted"


try:
    result = delete_user(user={"role": "admin"})
    print(f"SUCCESS: {result}")
except Exception as exc:
    print(exc)


try:
    delete_user(user={"role": "viewer"})
except PermissionError as exc:
    print(f"EXPECTED FAILURE: {exc}")


try:
    delete_user()
except ValueError as exc:
    print(f"EXPECTED FAILURE: {exc}")


print()
print("=" * 20)
print("DEMO COMPLETE")
print("=" * 20)
