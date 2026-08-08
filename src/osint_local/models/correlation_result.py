"""Modelos utilizados na correlação de dados públicos."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CorrelationStatus(str, Enum):
    """Estados possíveis de uma correlação."""

    CONFIRMED = "confirmado"
    CANDIDATE = "candidato"
    ABSENT = "ausente"
    INCONCLUSIVE = "inconclusivo"
    BLOCKED = "bloqueado"
    ERROR = "erro"


@dataclass
class CorrelationResult:
    """Representa uma informação encontrada durante uma correlação."""

    source: str
    category: str
    value: str
    status: CorrelationStatus
    source_url: str | None = None
    relationship: str | None = None
    checked_at: datetime = field(default_factory=datetime.now)
    evidence: list[str] = field(default_factory=list)
    notes: str | None = None
