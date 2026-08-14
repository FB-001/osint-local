"""Contexto consolidado fornecido à IA de propaganda."""

from dataclasses import dataclass, field

from perspicio.analysis.propaganda.analysis import PropagandaAnalysis
from perspicio.analysis.propaganda.vision.colors import summarize_colors
from perspicio.analysis.propaganda.vision.detections import DetectionStatus
from perspicio.analysis.propaganda.vision.labels import translate_yolo_label


@dataclass
class PropagandaAIContext:
    """Representa somente dados validados que podem ser enviados à IA."""

    texts: list[str] = field(default_factory=list)
    visual_elements: list[str] = field(default_factory=list)
    colors: list[str] = field(default_factory=list)
    slogan: str | None = None


def build_ai_context(
    analysis: PropagandaAnalysis,
) -> PropagandaAIContext:
    """Constrói o contexto da IA usando somente dados consolidados."""

    visual_elements = [
        translate_yolo_label(element.label)
        for element in analysis.observed.visual_elements
        if element.status == DetectionStatus.VALIDATED
    ]

    color_summary = summarize_colors(
        analysis.observed.colors
    )

    colors = [
        f"{name} — {proportion:.2f}%"
        for name, proportion in color_summary.items()
    ]

    return PropagandaAIContext(
        texts=list(analysis.observed.texts),
        visual_elements=visual_elements,
        colors=colors,
        slogan=analysis.slogan,
    )
