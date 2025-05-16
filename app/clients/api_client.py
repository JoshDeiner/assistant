import requests
from abc import ABC, abstractmethod

class ApiClient(ABC):
    @property
    @abstractmethod
    def BASE_URL(self) -> str:
        pass

    def __init__(self, params: dict = None):
        self.params = params or {}

    def fetch(self) -> dict:
        try:
            response = self._make_request()
            return self.parse_response(response.json())
        except Exception as e:
            return {"error": str(e)}

    def _make_request(self) -> requests.Response:
        return requests.get(self.BASE_URL, params=self.params, timeout=5)

    @abstractmethod
    def parse_response(self, data: dict) -> dict:
        pass
