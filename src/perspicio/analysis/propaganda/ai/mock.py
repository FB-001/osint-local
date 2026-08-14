"""Provedor de IA simulado para testes da análise de propaganda."""

from perspicio.analysis.propaganda.ai.base import PropagandaAI
from perspicio.analysis.propaganda.ai.context import PropagandaAIContext
from perspicio.analysis.propaganda.ai.result import (
    AIInference,
    PropagandaAIResult,
)


class MockPropagandaAI(PropagandaAI):
    """Simula uma IA sem utilizar um modelo real."""

    def analyze(
        self,
        context: PropagandaAIContext,
    ) -> PropagandaAIResult:
        """Retorna inferências simuladas para teste."""

        return PropagandaAIResult(
            force_idea=AIInference(
                value="Valorização da identidade do marinheiro",
                confidence=0.85,
                rationale=(
                    "Inferência simulada para testar "
                    "a arquitetura da aplicação."
                ),
            ),
        )
