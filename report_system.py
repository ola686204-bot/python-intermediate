"""SOLID-Based report generation and delivery system."""

from abc import ABC, abstractmethod
import json

class ReportAnalyzer(ABC):
    @abstractmethod
    def analyze(self, data):
        pass

class SummaryAnalyzer(ReportAnalyzer):
    def __init__(self):
        pass
    def analyze(self, data):
        total = sum(row['amount'] for row in data)
        count = len(data)
        average = total / count if count else 0

        return{
            "Total": total,
            "Count": count,
            "Average": average
        } 

class ReportFormatter(ABC):
    @abstractmethod
    def format(self, summary):
        pass
class TextFormatter(ReportFormatter):
    def __init__(self):
        pass
    def format(self,summary):
        return{
            f"Total: {summary['total']} |"
            f"Count: {summary['count']} |"
            f"Average: {summary['average']:.2f}"
        }
