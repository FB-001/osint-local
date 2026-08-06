"""Modelo do resultado de uma consulta de nome de usuário."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class UsernameStatus(str, Enum):
    """Estados possíveis de uma consulta de nome de usuário."""

    CONFIRMED = "confirmado"
    ABSENT = "ausente"
    INCONCLUSIVE = "inconclusivo"
    BLOCKED = "bloqueado"
    ERROR = "erro"


@dataclass
class UsernameResult:
    """Representa o resultado obtido em uma plataforma pública."""

    username: str
    platform: str
    profile_url: str
    status: UsernameStatus
    status_code: int | None = None
    response_time_ms: float | None = None
    checked_at: datetime = field(default_factory=datetime.now)
    evidence: list[str] = field(default_factory=list)
    notes: str | None = None
