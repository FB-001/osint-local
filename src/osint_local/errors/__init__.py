"""Exceções públicas do OSINT Local."""

from osint_local.errors.base import OsintLocalError
from osint_local.errors.hash import (
    HashAnalysisError,
    HashCalculationError,
    HashFileNotFoundError,
    HashPermissionError,
)
from osint_local.errors.image import (
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
