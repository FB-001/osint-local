"""Estruturas para detecções visuais automáticas."""

from dataclasses import dataclass


@dataclass
class VisualDetection:
    """Representa um elemento visual detectado automaticamente."""

    label: str
    confidence: float
    validated: bool = False
