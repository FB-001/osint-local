"""Formatadores de mensagens da interface do operador."""

from osint_local.ui.icons import COMMAND, ERROR, SUCCESS, WARNING


def format_command(
    command: str,
    description: str,
) -> str:
    """Formata um comando e sua descrição."""

    return "\n".join(
        [
            f"{COMMAND} {command}",
            "",
            f"    {description}",
        ]
    )


def format_success(message: str) -> str:
    """Formata uma mensagem de sucesso."""

    return f"{SUCCESS} {message}"


def format_warning(message: str) -> str:
    """Formata uma mensagem de aviso."""

    return f"{WARNING} {message}"


def format_error(message: str) -> str:
    """Formata uma mensagem de erro."""

    return f"{ERROR} {message}"
