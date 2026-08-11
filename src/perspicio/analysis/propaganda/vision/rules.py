"""Regras simples para geração de sugestões de análise."""

from perspicio.analysis.propaganda.observations import PropagandaObservations
from perspicio.analysis.propaganda.ocr import OcrTextStatus
from perspicio.analysis.propaganda.vision.base import AnalysisSuggestion
from perspicio.analysis.propaganda.vision.draft import PropagandaAnalysisDraft


def generate_suggestions(
    observed: PropagandaObservations,
) -> PropagandaAnalysisDraft:
    """Gera sugestões iniciais a partir dos dados observados."""

    draft = PropagandaAnalysisDraft()

    validated_texts = [
        item.final_text
        for item in observed.ocr_texts
        if item.status in {
            OcrTextStatus.VALIDATED,
            OcrTextStatus.CORRECTED,
        }
    ]

    if validated_texts:
        candidate = " ".join(validated_texts)

        draft.slogan = AnalysisSuggestion(
            value=candidate,
            confidence=0.90,
            rationale=(
                "Frase textual de destaque identificada automaticamente "
                "e posteriormente validada pelo operador."
            ),
            validated=False,
        )

    return draft
