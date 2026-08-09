"""Apresentação do resultado da comparação entre arquivos."""

from perspicio.models.hash_comparison import HashComparison
from perspicio.ui.console import (
    format_footer,
    format_header,
    format_paragraph,
    format_section,
)
from perspicio.ui.formatters import (
    format_success,
    format_warning,
)


def format_hash_comparison(comparison: HashComparison) -> str:
    """Retorna um relatório textual da comparação SHA-256."""

    if comparison.files_are_identical:
        result = format_success(
            "Os arquivos são idênticos em nível de bytes."
        )
    else:
        result = format_warning(
            "Os arquivos possuem conteúdos diferentes."
        )

    lines = [
        format_header("Comparação de integridade"),
        "",
        format_section("Arquivo A"),
        "",
        f"Nome: {comparison.first_file.name}",
        "",
        "SHA-256:",
        comparison.first_sha256,
        "",
        format_section("Arquivo B"),
        "",
        f"Nome: {comparison.second_file.name}",
        "",
        "SHA-256:",
        comparison.second_sha256,
        "",
        format_section("Resultado"),
        "",
        result,
        "",
        format_paragraph(
            "Observação: hashes diferentes comprovam que os arquivos "
            "diferem, mas não determinam isoladamente a causa ou a "
            "intenção da alteração."
        ),
        "",
        format_footer(),
    ]

    return "\n".join(lines)
