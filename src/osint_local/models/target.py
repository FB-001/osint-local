"""Modelo que representa um alvo de investigação."""

from dataclasses import dataclass, field


@dataclass
class Target:
    """Representa uma pessoa ou entidade investigada."""

    full_name: str
    cpf: str | None = None
    phone_numbers: list[str] = field(default_factory=list)
    emails: list[str] = field(default_factory=list)
    addresses: list[str] = field(default_factory=list)
