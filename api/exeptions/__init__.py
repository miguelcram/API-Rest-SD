from typing import Any

from bottle import response


class APIError(Exception):
    def __init__(self, status: int, message: Any, **kwargs):
        self.status = status
        self.message = message
        response.status = status
        response.message = message
        for key, value in kwargs.items():
            setattr(self, key, value)


class NotFound(APIError):
    def __init__(self):
        super().__init__(404, "Not Found")


class ValidationError(APIError):
    def __init__(self, **kwargs):
        super().__init__(400, "Bad Request", **kwargs)


__all__ = ["NotFound", "APIError"]
