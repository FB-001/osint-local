"""Regras simples para geração de sugestões de análise."""

from perspicio.analysis.propaganda.observations import PropagandaObservations
from perspicio.analysis.propaganda.vision.base import AnalysisSuggestion
from perspicio.analysis.propaganda.vision.draft import PropagandaAnalysisDraft


def generate_suggestions(
    observed: PropagandaObservations,
) -> PropagandaAnalysisDraft:
    """Gera sugestões iniciais a partir dos dados observados."""

    draft = PropagandaAnalysisDraft()

    if observed.texts:
        candidate = " ".join(observed.texts)

        draft.content = AnalysisSuggestion(
            value=candidate,
            confidence=0.60,
            rationale=(
                "Texto identificado pelo OCR com confiança mínima "
                "suficiente para análise preliminar."
            ),
            validated=False,
        )

    return draft
