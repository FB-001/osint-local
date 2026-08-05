"""Componentes reutilizáveis da interface textual."""

from textwrap import wrap

from osint_local.ui.theme import PRIMARY_LINE, SECONDARY_LINE, WIDTH


def format_header(title: str) -> str:
    """Retorna um cabeçalho principal padronizado."""

    return "\n".join(
        [
            PRIMARY_LINE,
            title.upper(),
            PRIMARY_LINE,
        ]
    )


def format_section(title: str) -> str:
    """Retorna o título de uma seção."""

    return "\n".join(
        [
            SECONDARY_LINE,
            title.upper(),
            SECONDARY_LINE,
        ]
    )


def format_footer() -> str:
    """Retorna o rodapé padrão."""

    return PRIMARY_LINE


def format_field(
    label: str,
    value: str,
    width: int = 20,
) -> str:
    """Retorna um campo alinhado com pontos."""

    dots = "." * max(1, width - len(label))

    return f"{label}{dots} {value}"


def format_paragraph(text: str, indent: int = 0) -> str:
    """Quebra um texto longo respeitando a largura da interface."""

    prefix = " " * indent
    available_width = WIDTH - indent

    lines = wrap(
        text,
        width=available_width,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return "\n".join(f"{prefix}{line}" for line in lines)


def format_warning(message: str) -> str:
    """Retorna uma mensagem de aviso."""

    return f"{WARNING} {message}"


def format_error(message: str) -> str:
    """Retorna uma mensagem de erro."""

    return f"{ERROR} {message}"
