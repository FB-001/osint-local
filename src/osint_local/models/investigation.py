"""Modelo que representa uma investigação."""

from dataclasses import dataclass, field
from datetime import datetime

from osint_local.models.evidence import Evidence
from osint_local.models.target import Target


@dataclass
class Investigation:
    """Representa um caso de investigação OSINT."""

    name: str
    analyst: str
    description: str
    status: str = "open"
    created_at: datetime = field(default_factory=datetime.now)
    targets: list[Target] = field(default_factory=list)
    evidences: list[Evidence] = field(default_factory=list)

    def add_target(self, target: Target) -> None:
        """Adiciona um alvo à investigação."""
        self.targets.append(target)

    def add_evidence(self, evidence: Evidence) -> None:
        """Adiciona uma evidência à investigação."""
        self.evidences.append(evidence)
