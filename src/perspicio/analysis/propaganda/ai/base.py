"""Interface-base para provedores de IA na análise de propaganda."""

from abc import ABC, abstractmethod

from perspicio.analysis.propaganda.ai.context import PropagandaAIContext
from perspicio.analysis.propaganda.ai.result import PropagandaAIResult


class PropagandaAI(ABC):
    """Define o contrato para uma IA de análise de propaganda."""

    @abstractmethod
    def analyze(
        self,
        context: PropagandaAIContext,
    ) -> PropagandaAIResult:
        """Analisa o contexto e retorna sugestões estruturadas."""
