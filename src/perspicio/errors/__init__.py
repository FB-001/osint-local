"""Exceções públicas do PERSPICIO."""

from perspicio.errors.base import OsintLocalError
from perspicio.errors.hash import (
    HashAnalysisError,
    HashCalculationError,
    HashFileNotFoundError,
    HashPermissionError,
)
from perspicio.errors.image import (
    ImageAnalysisError,
    ImageFileNotFoundError,
    ImagePermissionError,
    InvalidImageError,
)
from .company import (
    CompanyError,
    CompanyNetworkError,
    CompanyNotFoundError,
    CompanyServiceError,
)

__all__ = [
    "OsintLocalError",
    "ImageAnalysisError",
    "ImageFileNotFoundError",
    "InvalidImageError",
    "ImagePermissionError",
    "HashAnalysisError",
    "HashFileNotFoundError",
    "HashPermissionError",
    "HashCalculationError",
]
