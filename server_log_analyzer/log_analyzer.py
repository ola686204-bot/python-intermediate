
"""Stream, filter, analyse, and export server log records.

The program supports large log files, date and level filtering,
statistics, paginated output, and sample log generation.
"""

import argparse
import re
import sys
from collections import Counter
from datetime import datetime
from itertools import islice



LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} "
    r"\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+"
    r"(?P<message>.*)$",
    re.IGNORECASE
)

RESPONSE_TIME_PATTERN = re.compile(
    r"\bresponse_time\s*=\s*(\d+(?:\.\d+)?)\s*(ms|s)?\b",
    re.IGNORECASE,
)

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def read_lines(filename):
    """Read a log file one line at a time.

    Args:
        filename (str): Path to the log file.

    Yields:
        str: One line from the log file, without its newline character.
    """
    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            yield line.rstrip("\r\n")


def parse_log_lines(lines):
    """Parse log lines and skip malformed records.

    Args:
        lines (iterable): An iterable of raw log lines.

    Yields:
        dict: Parsed records containing timestamp, level, message,
            response_time_ms, and raw.
    """
    for line in lines:
        match = LOG_PATTERN.match(line.strip())

        if not match:
            continue

        try:
            timestamp = datetime.strptime(
                match.group("timestamp"),
                "%Y-%m-%d %H:%M:%S",
            )
        except ValueError:
            continue

        level = match.group("level").upper()
        message = match.group("message").strip()
        response_match = RESPONSE_TIME_PATTERN.search(message)
        response_time_ms = None

        if response_match:
            response_time_ms = float(response_match.group(1))

            if response_match.group(2) and (
                response_match.group(2).lower() == "s"
            ):
                response_time_ms *= 1000

        yield {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "response_time_ms": response_time_ms,
            "raw": line,
        }


def filter_by_level(records, levels=None):
    """Filter records by one or more log levels.

    Args:
        records (iterable): Parsed log records.
        levels (iterable | None): Allowed levels, such as ERROR.
            None means all levels.

    Yields:
        dict: Records that match the selected levels.
    """
    if levels is None:
        yield from records
        return

    allowed_levels = {level.upper() for level in levels}

    for record in records:
        if record["level"] in allowed_levels:
            yield record


def filter_by_date(records, start_date=None, end_date=None):
    """Filter records using inclusive calendar-date boundaries.

    Args:
        records (iterable): Parsed log records.
        start_date (date | None): Earliest included date.
        end_date (date | None): Latest included date.

    Yields:
        dict: Records within the requested date range.
    """
    for record in records:
        record_date = record["timestamp"].date()

        if start_date is not None and record_date < start_date:
            continue

        if end_date is not None and record_date > end_date:
            continue

        yield record


def batch(records, size):
    """Yield lists containing at most size records.

    Args:
        records (iterable): Records to group into batches.
        size (int): Maximum number of records per batch.

    Yields:
        list: A batch of records.

    Raises:
        ValueError: If size is less than one.
    """
    if size < 1:
        raise ValueError("Batch size must be at least 1.")

    iterator = iter(records)

    while True:
        current_batch = list(islice(iterator, size))

        if not current_batch:
            break

        yield current_batch


class LogWindow:
    """Provide reusable pagination over an iterable of records."""

    def __init__(self, records, page_size=10):
        """Initialize the log window.

        Args:
            records (iterable): Records to display.
            page_size (int): Maximum number of records per page.

        Raises:
            ValueError: If page_size is less than one.
        """
        if page_size < 1:
            raise ValueError("Page size must be at least 1.")

        self._records = iter(records)
        self.page_size = page_size
        self.page_number = 0

    def next_page(self):
        """Return the next page of records.

        Returns:
            list: The next page, or an empty list when finished.
        """
        page = list(islice(self._records, self.page_size))

        if page:
            self.page_number += 1

        return page

    def __iter__(self):
        """Return this window as an iterator.

        Returns:
            LogWindow: This pagination object.
        """
        return self

    def __next__(self):
        """Return the next page or stop iteration.

        Returns:
            list: The next page of records.

        Raises:
            StopIteration: When no records remain.
        """
        page = self.next_page()

        if not page:
            raise StopIteration

        return page


def format_record(record):
    """Format a parsed record for terminal display.

    Args:
        record (dict): A parsed log record.

    Returns:
        str: A formatted record.
    """
    timestamp = record["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    return (
        f"{timestamp} {record['level']:<8} "
        f"{record['message']}"
    )


def display_pages(records, page_size=10, prompt=True):
    """Display records in pages.

    Args:
        records (iterable): Parsed records to display.
        page_size (int): Records per page.
        prompt (bool): Whether to ask before continuing.

    Returns:
        int: Number of records displayed.
    """
    window = LogWindow(records, page_size)
    displayed = 0

    for page in window:
        for record in page:
            print(format_record(record))
            displayed += 1

        if prompt:
            try:
                answer = input(
                    f"\nPage {window.page_number} displayed. "
                    "Press Enter for more or type q to stop: "
                ).strip().lower()
            except EOFError:
                break

            if answer == "q":
                break

    if displayed == 0:
        print("No matching log records found.")

    return displayed


def compute_statistics(records):
    """Calculate statistics from a single-pass record iterable.

    Args:
        records (iterable): Parsed records to analyse.

    Returns:
        dict: Counts, common errors, and response-time statistics.
    """
    total = 0
    level_counts = Counter()
    error_messages = Counter()
    response_time_total = 0.0
    response_time_count = 0

    for record in records:
        total += 1
        level_counts[record["level"]] += 1

        if record["level"] in {"ERROR", "CRITICAL"}:
            message = RESPONSE_TIME_PATTERN.sub(
                "",
                record["message"],
            ).strip()
            error_messages[message] += 1

        response_time = record["response_time_ms"]

        if response_time is not None:
            response_time_total += response_time
            response_time_count += 1

    average_response_time = (
        response_time_total / response_time_count
        if response_time_count
        else None
    )

    return {
        "total": total,
        "level_counts": {
            level: level_counts.get(level, 0)
            for level in LOG_LEVELS
        },
        "top_errors": error_messages.most_common(5),
        "average_response_time_ms": average_response_time,
        "response_time_count": response_time_count,
    }


def display_statistics(statistics):
    """Display calculated log statistics.

    Args:
        statistics (dict): Statistics from compute_statistics().

    Returns:
        None: This function displays the statistics.
    """
    print("\n--- Log Statistics ---")
    print(f"Total matching records: {statistics['total']}")
    print("Records by level:")

    for level, count in statistics["level_counts"].items():
        print(f"  {level}: {count}")

    print("Top 5 error messages:")

    if statistics["top_errors"]:
        for message, count in statistics["top_errors"]:
            print(f"  {count} occurrence(s): {message}")
    else:
        print("  No ERROR or CRITICAL messages found.")

    average = statistics["average_response_time_ms"]

    if average is None:
        print("Average response time: Not available")
    else:
        print(f"Average response time: {average:.2f} ms")
        print(
            "Records with response times: "
            f"{statistics['response_time_count']}"
        )


def export_records(records, filename):
    """Write filtered raw log records to a new file.

    Args:
        records (iterable): Parsed records to export.
        filename (str): Destination filename.

    Returns:
        int: Number of records exported.
    """
    count = 0

    with open(filename, "w", encoding="utf-8") as file:
        for record in records:
            file.write(record["raw"] + "\n")
            count += 1

    return count


def generate_sample_logs(filename, count=100):
    """Generate sample logs without storing all lines in memory.

    Args:
        filename (str): Destination file.
        count (int): Number of sample records to generate.

    Returns:
        int: Number of records written.
    """
    if count < 0:
        raise ValueError("Sample count cannot be negative.")

    levels = ("INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL")
    messages = (
        "Request completed response_time=120ms",
        "Database connection failed",
        "Authentication failed",
        "Cache miss response_time=0.25s",
        "Request completed response_time=80ms",
    )

    def sample_lines():
        """Yield sample log lines one at a time.

        Yields:
            str: One formatted sample log line.
        """
        for index in range(count):
            timestamp = datetime(2024, 1, 15, 12, 0, 0)
            from datetime import timedelta

            timestamp += timedelta(seconds=index)
            level = levels[index % len(levels)]
            message = messages[index % len(messages)]

            yield (
                f"{timestamp:%Y-%m-%d %H:%M:%S} "
                f"{level} {message}"
            )

    written = 0

    with open(filename, "w", encoding="utf-8") as file:
        for line in sample_lines():
            file.write(line + "\n")
            written += 1

    return written


def parse_date(value):
    """Parse a YYYY-MM-DD date argument.

    Args:
        value (str): Date text from the command line.

    Returns:
        date: Parsed calendar date.

    Raises:
        argparse.ArgumentTypeError: If the date is invalid.
    """
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"Invalid date {value!r}; use YYYY-MM-DD."
        ) from error


def build_parser():
    """Build the command-line argument parser.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Stream, filter, and analyse server logs."
    )
    parser.add_argument(
        "--input",
        help="Input log filename.",
    )
    parser.add_argument(
        "--level",
        nargs="+",
        choices=LOG_LEVELS,
        type=str.upper,
        help="One or more log levels to include.",
    )
    parser.add_argument(
        "--start-date",
        type=parse_date,
        help="Inclusive start date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--end-date",
        type=parse_date,
        help="Inclusive end date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--export",
        help="Export matching raw records to this filename.",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=10,
        help="Number of records to display per page (default: 10).",
    )
    parser.add_argument(
        "--no-prompt",
        action="store_true",
        help="Display all matching records without pagination prompts.",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Display statistics for matching records.",
    )
    parser.add_argument(
        "--generate-sample",
        metavar="FILENAME",
        help="Generate a sample log file and exit.",
    )
    parser.add_argument(
        "--sample-lines",
        type=int,
        default=100,
        help="Number of sample records to generate (default: 100).",
    )
    return parser


def build_pipeline(filename, levels=None, start_date=None, end_date=None):
    """Build a streaming pipeline for a log file.

    Args:
        filename (str): Input log filename.
        levels (iterable | None): Log levels to include.
        start_date (date | None): Inclusive start date.
        end_date (date | None): Inclusive end date.

    Returns:
        iterable: A generator yielding matching parsed records.
    """
    records = parse_log_lines(read_lines(filename))
    records = filter_by_level(records, levels)
    records = filter_by_date(records, start_date, end_date)
    return records


def main(argv=None):
    """Run the command-line log analyser.

    Args:
        argv (list | None): Optional command-line arguments.

    Returns:
        int: Exit status, where zero indicates success.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.page_size < 1:
        parser.error("--page-size must be at least 1.")

    if (
        args.start_date is not None
        and args.end_date is not None
        and args.start_date > args.end_date
    ):
        parser.error("--start-date cannot be later than --end-date.")

    if args.sample_lines < 0:
        parser.error("--sample-lines cannot be negative.")

    if args.generate_sample:
        try:
            count = generate_sample_logs(
                args.generate_sample,
                args.sample_lines,
            )
            print(
                f"Generated {count} sample records in "
                f"{args.generate_sample}"
            )
            return 0
        except OSError as error:
            print(f"Could not generate sample file: {error}", file=sys.stderr)
            return 1

    if not args.input:
        parser.error("--input is required unless --generate-sample is used.")

    try:
        if args.export:
            exported = export_records(
                build_pipeline(
                    args.input,
                    args.level,
                    args.start_date,
                    args.end_date,
                ),
                args.export,
            )
            print(f"Exported {exported} records to {args.export}")

        if args.stats:
            display_statistics(
                compute_statistics(
                    build_pipeline(
                        args.input,
                        args.level,
                        args.start_date,
                        args.end_date,
                    )
                )
            )

        display_pages(
            build_pipeline(
                args.input,
                args.level,
                args.start_date,
                args.end_date,
            ),
            page_size=args.page_size,
            prompt=not args.no_prompt,
        )

        return 0

    except (OSError, UnicodeError) as error:
        print(f"File error: {error}", file="app")
        return 


if __name__ == "__main__":
    raise SystemExit(main())
