from abc import ABC, abstractmethod


class SaveResultsToCSV(ABC):
    """Enforces saving results to .csv file functionality on descendants"""
    @abstractmethod
    def save_results_to_csv(self, directory):
        """Saves results in directory location"""


class SaveResultsToJSON(ABC):
    """Enforces saving results as .json file functionality on descendants"""
    @abstractmethod
    def save_results_to_json(self, directory):
        """Saves results in directory location"""
