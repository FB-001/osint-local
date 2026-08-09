"""Rascunho de análise automática de propaganda."""

from dataclasses import dataclass, field

from perspicio.analysis.propaganda.vision.base import AnalysisSuggestion


@dataclass
class PropagandaAnalysisDraft:
    """Representa sugestões automáticas ainda não validadas pelo operador."""

    propaganda_type: AnalysisSuggestion | None = None
    classification: AnalysisSuggestion | None = None

    credibility: AnalysisSuggestion | None = None
    coherence: AnalysisSuggestion | None = None
    significance: AnalysisSuggestion | None = None
    positivity: AnalysisSuggestion | None = None
    permanence: AnalysisSuggestion | None = None
    adequacy: AnalysisSuggestion | None = None
    opportunity: AnalysisSuggestion | None = None

    force_idea: AnalysisSuggestion | None = None
    theme: AnalysisSuggestion | None = None
    slogan: AnalysisSuggestion | None = None
    symbol: AnalysisSuggestion | None = None

    origin: AnalysisSuggestion | None = None
    content: AnalysisSuggestion | None = None
    target_audience: AnalysisSuggestion | None = None
    vehicle: AnalysisSuggestion | None = None
    effect: AnalysisSuggestion | None = None

    uncertainties: list[str] = field(default_factory=list)
