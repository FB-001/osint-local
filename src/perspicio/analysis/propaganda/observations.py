"""Dados observáveis extraídos de uma peça de propaganda."""

from dataclasses import dataclass, field


@dataclass
class PropagandaObservations:
    """Representa elementos diretamente observáveis na propaganda."""

    texts: list[str] = field(default_factory=list)
    visual_elements: list[str] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)
    colors: list[str] = field(default_factory=list)

@dataclass
class PropagandaObservations:
    raw_texts: list[str] = field(default_factory=list)
    texts: list[str] = field(default_factory=list)
    visual_elements: list[str] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)
    colors: list[str] = field(default_factory=list)
