"""Modelo que representa uma evidência."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Evidence:
    """Representa uma evidência vinculada a uma investigação."""

    evidence_type: str
    source: str
    description: str
    collected_at: datetime
    notes: str | None = None
