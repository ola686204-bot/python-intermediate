"""
Resource management framework for database sessions,
timing, CSV exports, and multi-resource coordination.

"""

import contextlib
import csv
import os
import sqlite3
import time
from dataclasses import dataclass
from functools import wraps


class ManagedDatabase:
    """
    Context manager for SQLite database sessions.

    Opens a database connection on entry and automatically
    commits, rolls back, and closes the connection on exit.

    Args:
        db_path (str):
            SQLite database path.

        isolation_level (str):
            SQLite transaction isolation level.
    """

    def __init__(
        self,
        db_path,
        isolation_level="deferred"
    ):
        self.db_path = db_path
        self.isolation_level = isolation_level
        self.connection = None

    def __enter__(self):
        """
        Open database connection.

        Returns:
            sqlite3.Connection:
                Active database connection.
        """
        self.connection = sqlite3.connect(
            self.db_path,
            isolation_level=self.isolation_level
        )

        self.connection.row_factory = sqlite3.Row

        return self.connection

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ):
        """
        Commit or rollback transaction
        and always close the connection.

        Args:
            exc_type:
                Exception class.

            exc_val:
                Exception instance.

            exc_tb:
                Traceback.
        """

        try:
            if exc_type is None:

                self.connection.commit()

                print(
                    "[DB] Transaction committed"
                )

            else:

                self.connection.rollback()

                print(
                    f"[DB] Transaction rolled back: "
                    f"{exc_val}"
                )

        finally:

            if self.connection:
                self.connection.close()

        return False


def managed_query(
    context_manager_factory
):
    """
    Decorator that automatically executes
    database functions inside a context manager.

    Args:
        context_manager_factory (callable):
            Callable returning a ManagedDatabase.

    Returns:
        callable:
            Decorated function.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            with context_manager_factory() as conn:

                return func(
                    conn,
                    *args,
                    **kwargs
                )

        return wrapper

    return decorator


@dataclass
class TimerResult:
    """
    Stores timing results.
    """

    elapsed_ms: float = 0.0


@contextlib.contextmanager
def timer(
    label="Operation",
    logger=None
):
    """
    Measure execution time.

    Args:
        label (str):
            Operation label.

        logger:
            Optional logger object
            supporting logger.info().

    Yields:
        TimerResult:
            Result object whose
            elapsed_ms is populated
            when the block exits.
    """

    result = TimerResult()

    start = time.perf_counter()

    try:
        yield result

    finally:

        end = time.perf_counter()

        result.elapsed_ms = (
            end - start
        ) * 1000

        message = (
            f"[TIMER] {label} "
            f"completed in "
            f"{result.elapsed_ms:.2f}ms"
        )

        if logger is None:

            print(message)

        else:

            logger.info(message)


@contextlib.contextmanager
def atomic_csv_writer(
    filepath,
    fieldnames,
    encoding="utf-8"
):
    """
    Atomically write CSV files.

    Writes to .tmp first.
    On success, replaces target file.
    On failure, removes temporary file.

    Args:
        filepath (str):
            Final CSV path.

        fieldnames (list):
            CSV header names.

        encoding (str):
            File encoding.

    Yields:
        csv.DictWriter
    """

    temp_path = filepath + ".tmp"

    file_handle = None

    try:

        file_handle = open(
            temp_path,
            mode="w",
            newline="",
            encoding=encoding
        )

        writer = csv.DictWriter(
            file_handle,
            fieldnames=fieldnames
        )

        writer.writeheader()

        yield writer

        file_handle.close()

        os.replace(
            temp_path,
            filepath
        )

    except Exception:

        if file_handle and not file_handle.closed:
            file_handle.close()

        if os.path.exists(temp_path):
            os.remove(temp_path)

        raise


@contextlib.contextmanager
def multi_resource(
    *context_managers
):
    """
    Enter multiple context managers
    and yield their values.

    Uses ExitStack internally.

    Args:
        *context_managers:
            Context manager instances.

    Yields:
        tuple:
            Values returned from all
            context manager __enter__ calls.
    """

    with contextlib.ExitStack() as stack:

        resources = tuple(
            stack.enter_context(cm)
            for cm in context_managers
        )

        yield resources
