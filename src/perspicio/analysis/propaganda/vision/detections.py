"""Estruturas para detecções visuais automáticas."""

from dataclasses import dataclass
from enum import Enum


class DetectionStatus(str, Enum):
    """Estados possíveis de uma detecção visual."""

    PENDING = "pending"
    VALIDATED = "validated"
    REJECTED = "rejected"


@dataclass
class VisualDetection:
    """Representa um elemento visual detectado automaticamente."""

    label: str
    confidence: float
    status: DetectionStatus = DetectionStatus.PENDING
