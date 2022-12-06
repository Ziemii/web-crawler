from abc import ABC, abstractmethod


class ResultsPrinter(ABC):
    """Enforces results printing functionality on descendants"""

    @abstractmethod
    def print_results(self):
        """Prints results"""
