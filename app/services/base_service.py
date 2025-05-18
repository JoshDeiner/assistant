from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        """Main execution logic for the service."""
        pass