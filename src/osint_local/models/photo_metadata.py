"""Modelo dos metadados extraídos de uma imagem."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class PhotoMetadata:
    """Representa informações técnicas extraídas de uma fotografia."""

    file_path: Path
    device_model: str | None
    captured_at: datetime | None
    latitude: float | None
    longitude: float | None
    width: int
    height: int
    file_size_bytes: int
    sha256: str
