"""Revisão e validação de sugestões de análise de propaganda."""

from perspicio.analysis.propaganda.analysis import PropagandaAnalysis
from perspicio.analysis.propaganda.vision.draft import PropagandaAnalysisDraft


def apply_validated_draft(
    analysis: PropagandaAnalysis,
    draft: PropagandaAnalysisDraft,
) -> PropagandaAnalysis:
    """Aplica à análise final somente sugestões validadas pelo operador."""

    if draft.propaganda_type and draft.propaganda_type.validated:
        analysis.propaganda_type = draft.propaganda_type.value

    if draft.classification and draft.classification.validated:
        analysis.classification = draft.classification.value

    if draft.credibility and draft.credibility.validated:
        analysis.credibility = draft.credibility.value

    if draft.coherence and draft.coherence.validated:
        analysis.coherence = draft.coherence.value

    if draft.significance and draft.significance.validated:
        analysis.significance = draft.significance.value

    if draft.positivity and draft.positivity.validated:
        analysis.positivity = draft.positivity.value

    if draft.permanence and draft.permanence.validated:
        analysis.permanence = draft.permanence.value

    if draft.adequacy and draft.adequacy.validated:
        analysis.adequacy = draft.adequacy.value

    if draft.opportunity and draft.opportunity.validated:
        analysis.opportunity = draft.opportunity.value

    if draft.force_idea and draft.force_idea.validated:
        analysis.force_idea = draft.force_idea.value

    if draft.theme and draft.theme.validated:
        analysis.theme = draft.theme.value

    if draft.slogan and draft.slogan.validated:
        analysis.slogan = draft.slogan.value

    if draft.symbol and draft.symbol.validated:
        analysis.symbol = draft.symbol.value

    if draft.origin and draft.origin.validated:
        analysis.ocave.origin = draft.origin.value

    if draft.content and draft.content.validated:
        analysis.ocave.content = draft.content.value

    if draft.target_audience and draft.target_audience.validated:
        analysis.ocave.target_audience = draft.target_audience.value

    if draft.vehicle and draft.vehicle.validated:
        analysis.ocave.vehicle = draft.vehicle.value

    if draft.effect and draft.effect.validated:
        analysis.ocave.effect = draft.effect.value

    return analysis
