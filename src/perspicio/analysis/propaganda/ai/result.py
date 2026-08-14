"""Estruturas para resultados produzidos pela IA na análise de propaganda."""

from dataclasses import dataclass, field


@dataclass(slots=True)
class AIInference:
    """Representa uma inferência produzida pela IA."""

    value: str
    confidence: float | None = None
    rationale: str | None = None


@dataclass(slots=True)
class PropagandaAIResult:
    """Representa as sugestões analíticas produzidas pela IA."""

    propaganda_type: AIInference | None = None
    classification: AIInference | None = None

    credibility: AIInference | None = None
    coherence: AIInference | None = None
    significance: AIInference | None = None
    positivity: AIInference | None = None
    permanence: AIInference | None = None
    adequacy: AIInference | None = None
    opportunity: AIInference | None = None

    force_idea: AIInference | None = None
    theme: AIInference | None = None

    origin: AIInference | None = None
    content: AIInference | None = None
    target_audience: AIInference | None = None
    vehicle: AIInference | None = None
    effect: AIInference | None = None

    uncertainties: list[str] = field(default_factory=list)
