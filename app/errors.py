# app/errors.py

from typing import Any, Optional


class AppValidationError(Exception):
    def __init__(
        self,
        message: str = "Validation failed",
        errors: Optional[dict[str, list[str]]] = None,
        status_code: int = 422,
    ):
        self.message = message
        self.errors = errors or {}
        self.status_code = status_code
