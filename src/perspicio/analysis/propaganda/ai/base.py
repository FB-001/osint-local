"""Contrato-base para análise de propaganda assistida por IA."""

from abc import ABC, abstractmethod

from perspicio.analysis.propaganda.ai.context import PropagandaAIContext
from perspicio.analysis.propaganda.vision.draft import PropagandaAnalysisDraft


class PropagandaAI(ABC):
    """Define o contrato para mecanismos de análise assistida por IA."""

    @abstractmethod
    def analyze(
        self,
        context: PropagandaAIContext,
    ) -> PropagandaAnalysisDraft:
        """Gera sugestões analíticas a partir de dados validados."""
