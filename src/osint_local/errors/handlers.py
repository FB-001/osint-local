"""Apresentação centralizada dos erros ao operador."""

from pathlib import Path

from osint_local.ui.console import (
    format_footer,
    format_header,
    format_paragraph,
)
from osint_local.ui.formatters import format_error


def format_operator_error(
    message: str,
    path: Path | None = None,
    guidance: str | None = None,
) -> str:
    """Retorna uma mensagem de erro clara para o operador."""

    lines = [
        format_header("Erro"),
        "",
        format_error(message),
    ]

    if path is not None:
        lines.extend(
            [
                "",
                "Caminho informado:",
                format_paragraph(str(path), indent=4),
            ]
        )

    if guidance:
        lines.extend(
            [
                "",
                "Como resolver:",
                format_paragraph(guidance, indent=4),
            ]
        )

    lines.extend(
        [
            "",
            format_footer(),
        ]
    )

    return "\n".join(lines)
