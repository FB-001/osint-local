"""Modelo geral para análise estruturada de propaganda."""

from dataclasses import dataclass, field

from perspicio.analysis.propaganda.ocave import OcaveAnalysis

from perspicio.analysis.propaganda.observations import PropagandaObservations


@dataclass(slots=True)
class PropagandaAnalysis:
    """Representa uma análise estruturada de uma peça de propaganda."""

    identification: str
    observed: PropagandaObservations = field(
        default_factory=PropagandaObservations
    )

    propaganda_type: str | None = None
    classification: str | None = None

    credibility: str | None = None
    coherence: str | None = None
    significance: str | None = None
    positivity: str | None = None
    permanence: str | None = None
    adequacy: str | None = None
    opportunity: str | None = None

    force_idea: str | None = None
    theme: str | None = None
    slogan: str | None = None
    symbol: str | None = None

    ocave: OcaveAnalysis = field(default_factory=OcaveAnalysis)

    observations: str | None = None
