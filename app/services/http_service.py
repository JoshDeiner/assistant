from typing import Any
from typing import Dict

from requests import Response
from requests import get


class RequestsHTTPService:
    """
    A simple HTTP service implementation using the `requests` library.
    """
    def get(self, url: str, params: Dict[str, Any], timeout: float) -> Response:
        return get(url, params=params, timeout=timeout)


