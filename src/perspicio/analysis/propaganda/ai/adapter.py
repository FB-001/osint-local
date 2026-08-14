"""Conversão de resultados da IA para sugestões revisáveis."""

from perspicio.analysis.propaganda.ai.result import (
    AIInference,
    PropagandaAIResult,
)
from perspicio.analysis.propaganda.vision.base import AnalysisSuggestion
from perspicio.analysis.propaganda.vision.draft import PropagandaAnalysisDraft


def _to_suggestion(
    inference: AIInference | None,
) -> AnalysisSuggestion | None:
    """Converte uma inferência da IA em sugestão revisável."""

    if inference is None:
        return None

    return AnalysisSuggestion(
        value=inference.value,
        confidence=inference.confidence,
        rationale=inference.rationale,
        validated=False,
    )


def ai_result_to_draft(
    result: PropagandaAIResult,
) -> PropagandaAnalysisDraft:
    """Converte o resultado da IA em rascunho de análise."""

    return PropagandaAnalysisDraft(
        propaganda_type=_to_suggestion(result.propaganda_type),
        classification=_to_suggestion(result.classification),

        credibility=_to_suggestion(result.credibility),
        coherence=_to_suggestion(result.coherence),
        significance=_to_suggestion(result.significance),
        positivity=_to_suggestion(result.positivity),
        permanence=_to_suggestion(result.permanence),
        adequacy=_to_suggestion(result.adequacy),
        opportunity=_to_suggestion(result.opportunity),

        force_idea=_to_suggestion(result.force_idea),
        theme=_to_suggestion(result.theme),

        origin=_to_suggestion(result.origin),
        content=_to_suggestion(result.content),
        target_audience=_to_suggestion(result.target_audience),
        vehicle=_to_suggestion(result.vehicle),
        effect=_to_suggestion(result.effect),

        uncertainties=list(result.uncertainties),
    )
