"""Modelo para análise de propaganda pelo método OCAVE."""

from dataclasses import dataclass


@dataclass(slots=True)
class OcaveAnalysis:
    """Representa os cinco elementos da análise OCAVE."""

    origin: str | None = None
    content: str | None = None
    target_audience: str | None = None
    vehicle: str | None = None
    effect: str | None = None
