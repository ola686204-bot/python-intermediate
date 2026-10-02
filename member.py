"""SOLID-based report generation and delivery system."""

from abc import ABC, abstractmethod
import json


class ReportAnalyzer(ABC):
    """Define the interface for analyzing report data."""

    @abstractmethod
    def analyze(self, data):
        """Analyze report data and return a summary.

        Args:
            data (list): Report rows containing an amount field.

        Returns:
            dict: Summary containing total, count, and average.
        """
        pass


class SummaryAnalyzer(ReportAnalyzer):
    """Calculate summary statistics from report data."""

    def __init__(self):
        """Initialize the summary analyzer."""
        pass

    def analyze(self, data):
        """Calculate total, count, and average from report data.

        Args:
            data (list): Report rows containing an amount field.

        Returns:
            dict: Summary with total, count, and average.
        """
        total = sum(row["amount"] for row in data)
        count = len(data)
        average = total / count if count else 0

        return {
            "total": total,
            "count": count,
            "average": average,
        }


class ReportFormatter(ABC):
    """Define the interface for formatting report summaries."""

    @abstractmethod
    def format(self, summary):
        """Format a report summary into a string.

        Args:
            summary (dict): Summary containing report statistics.

        Returns:
            str: Formatted report content.
        """
        pass


class TextFormatter(ReportFormatter):
    """Format report summaries as plain text."""

    def __init__(self):
        """Initialize the text formatter."""
        pass

    def format(self, summary):
        """Format the summary as readable plain text.

        Args:
            summary (dict): Report summary.

        Returns:
            str: Plain-text report.
        """
        return (
            f"Total: {summary['total']} | "
            f"Count: {summary['count']} | "
            f"Average: {summary['average']:.2f}"
        )


class CSVFormatter(ReportFormatter):
    """Format report summaries as CSV."""

    def __init__(self):
        """Initialize the CSV formatter."""
        pass

    def format(self, summary):
        """Format the summary as CSV data.

        Args:
            summary (dict): Report summary.

        Returns:
            str: CSV-formatted report.
        """
        return (
            "total,count,average\n"
            f"{summary['total']},"
            f"{summary['count']},"
            f"{summary['average']:.2f}"
        )


class JSONFormatter(ReportFormatter):
    """Format report summaries as JSON."""

    def __init__(self):
        """Initialize the JSON formatter."""
        pass

    def format(self, summary):
        """Format the summary as JSON.

        Args:
            summary (dict): Report summary.

        Returns:
            str: JSON-formatted report.
        """
        return json.dumps(summary, indent=2)


class ReportDelivery(ABC):
    """Define the interface for delivering formatted reports."""

    @abstractmethod
    def deliver(self, content):
        """Deliver report content.

        Args:
            content (str): Formatted report content.
        """
        pass


class ConsoleDelivery(ReportDelivery):
    """Deliver reports by displaying them in the console."""

    def __init__(self):
        """Initialize console delivery."""
        pass

    def deliver(self, content):
        """Print the report content to the console.

        Args:
            content (str): Formatted report content.
        """
        print("\n--- Console Delivery ---")
        print(content)


class FileDelivery(ReportDelivery):
    """Deliver reports by saving them to a file."""

    def __init__(self, filename):
        """Initialize file delivery.

        Args:
            filename (str): File path where the report will be saved.
        """
        self.filename = filename

    def deliver(self, content):
        """Save the report content to a file.

        Args:
            content (str): Formatted report content.
        """
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"\nReport saved to: {self.filename}")


class EmailDelivery(ReportDelivery):
    """Simulate delivering a report by email."""

    def __init__(self, recipient):
        """Initialize email delivery.

        Args:
            recipient (str): Email address of the recipient.
        """
        self.recipient = recipient

    def deliver(self, content):
        """Simulate sending report content by email.

        Args:
            content (str): Formatted report content.
        """
        print("\n--- Email Delivery ---")
        print(f"Sending report to: {self.recipient}")
        print(content)
        print("Email sent successfully.")


class ReportService:
    """Coordinate analysis, formatting, and delivery of reports."""

    def __init__(self, analyzer, formatter, delivery):
        """Initialize the report service with injected dependencies.

        Args:
            analyzer (ReportAnalyzer): Object that analyzes report data.
            formatter (ReportFormatter): Object that formats the summary.
            delivery (ReportDelivery): Object that delivers the report.
        """
        self.analyzer = analyzer
        self.formatter = formatter
        self.delivery = delivery

    def generate_and_deliver(self, data):
        """Analyze, format, and deliver a report.

        Args:
            data (list): Report rows containing an amount field.

        Returns:
            str: The formatted report content.
        """
        summary = self.analyzer.analyze(data)
        content = self.formatter.format(summary)
        self.delivery.deliver(content)

        return content


def main():
    """Demonstrate the report system with multiple formatters and deliveries."""
    data = [
        {"amount": 100},
        {"amount": 250},
        {"amount": 150},
        {"amount": 300},
    ]

    analyzer = SummaryAnalyzer()

    text_formatter = TextFormatter()
    console_delivery = ConsoleDelivery()

    text_service = ReportService(
        analyzer,
        text_formatter,
        console_delivery,
    )

    text_service.generate_and_deliver(data)

    csv_formatter = CSVFormatter()
    file_delivery = FileDelivery("report.csv")

    csv_service = ReportService(
        analyzer,
        csv_formatter,
        file_delivery,
    )

    csv_service.generate_and_deliver(data)

    json_formatter = JSONFormatter()
    email_delivery = EmailDelivery("library@example.com")

    json_service = ReportService(
        analyzer,
        json_formatter,
        email_delivery,
    )

    json_service.generate_and_deliver(data)


if __name__ == "__main__":
    main()
