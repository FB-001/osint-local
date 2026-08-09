"""Dados observáveis extraídos de uma peça de propaganda."""

from dataclasses import dataclass, field

from perspicio.analysis.propaganda.vision.colors import ObservedColor
from perspicio.analysis.propaganda.vision.detections import VisualDetection

@dataclass
class PropagandaObservations:
    """Representa elementos diretamente observáveis na propaganda."""

    raw_texts: list[str] = field(default_factory=list)
    texts: list[str] = field(default_factory=list)
    visual_elements: list[VisualDetection] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)
    colors: list[ObservedColor] = field(default_factory=list)
