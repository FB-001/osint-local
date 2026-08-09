"""Estruturas-base para análise visual assistida de propaganda."""

from dataclasses import dataclass


@dataclass
class AnalysisSuggestion:
    """Representa uma inferência automática ainda não validada."""

    value: str
    confidence: float | None = None
    rationale: str | None = None
    validated: bool = False
