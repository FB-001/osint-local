"""Apresentação de análises estruturadas de propaganda."""

from perspicio.analysis.propaganda.analysis import PropagandaAnalysis
from perspicio.ui.console import (
    format_field,
    format_footer,
    format_header,
    format_section,
)


def _value_or_undetermined(value: str | None) -> str:
    """Retorna um valor legível quando não houver conclusão."""

    if value is None or not value.strip():
        return "Não determinado"

    return value


def _value_or_not_informed(value: str | None) -> str:
    """Retorna um valor legível para campos opcionais."""

    if value is None or not value.strip():
        return "Não informado"

    return value


def format_propaganda_analysis(analysis: PropagandaAnalysis) -> str:
    """Formata uma análise estruturada de propaganda."""

    lines = [
        format_header("ANÁLISE DE PROPAGANDA"),
        "",
        format_section("Identificação"),
        "",
        format_field(
            "Propaganda",
            analysis.identification,
        ),
        "",
        format_section("Caracterização"),
        "",
        format_field(
            "Tipo",
            _value_or_undetermined(analysis.propaganda_type),
        ),
        format_field(
            "Classificação",
            _value_or_undetermined(analysis.classification),
        ),
        "",
        format_section("Princípios"),
        "",
        format_field(
            "Credibilidade",
            _value_or_undetermined(analysis.credibility),
        ),
        format_field(
            "Coerência",
            _value_or_undetermined(analysis.coherence),
        ),
        format_field(
            "Significância",
            _value_or_undetermined(analysis.significance),
        ),
        format_field(
            "Positividade",
            _value_or_undetermined(analysis.positivity),
        ),
        format_field(
            "Permanência",
            _value_or_undetermined(analysis.permanence),
        ),
        format_field(
            "Adequabilidade",
            _value_or_undetermined(analysis.adequacy),
        ),
        format_field(
            "Oportunidade",
            _value_or_undetermined(analysis.opportunity),
        ),
        "",
        format_section("Elementos essenciais"),
        "",
        format_field(
            "Ideia-força",
            _value_or_undetermined(analysis.force_idea),
        ),
        format_field(
            "Tema",
            _value_or_undetermined(analysis.theme),
        ),
        format_field(
            "Frase-síntese",
            _value_or_undetermined(analysis.slogan),
        ),
        format_field(
            "Símbolo",
            _value_or_undetermined(analysis.symbol),
        ),
        "",
        format_section("OCAVE"),
        "",
        format_field(
            "Origem",
            _value_or_undetermined(analysis.ocave.origin),
        ),
        format_field(
            "Conteúdo",
            _value_or_undetermined(analysis.ocave.content),
        ),
        format_field(
            "Audiência-alvo",
            _value_or_undetermined(analysis.ocave.target_audience),
        ),
        format_field(
            "Veículo de difusão",
            _value_or_undetermined(analysis.ocave.vehicle),
        ),
        format_field(
            "Efeito",
            _value_or_undetermined(analysis.ocave.effect),
        ),
        "",
        format_section("Observações do operador"),
        "",
        _value_or_not_informed(analysis.observations),
        "",
        format_footer(),
    ]

    return "\n".join(lines)
