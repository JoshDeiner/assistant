class ApiError(Exception):
    """Base class for API-related errors."""
    def __init__(self, message: str, status_code: int = 1):
        super().__init__(message)
        self.status_code = status_code

class CryptoPriceError(ApiError):
    """Raised when there is an error fetching cryptocurrency prices."""
    def __init__(self, message: str = "Failed to fetch cryptocurrency price.", status_code: int = 1):
        super().__init__(message, status_code)
