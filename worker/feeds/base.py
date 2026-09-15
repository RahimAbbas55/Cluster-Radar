from abc import ABC, abstractmethod

class FeedChecker(ABC):
    # every feed source implements this interface
    name: str

    @abstractmethod
    def fetch(self):
        # returns (data, latency_ms, error_message)
        # data is the raw value used to detect staleness (e.g. a price or timestamp)
        pass