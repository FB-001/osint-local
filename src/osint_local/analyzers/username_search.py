"""Orquestra consultas de nomes de usuário em múltiplas fontes."""

from osint_local.collectors.registry import (
    REGISTERED_USERNAME_COLLECTORS,
    UsernameCollector,
)
from osint_local.models.username_result import UsernameResult


def search_username(
    username: str,
    collectors: tuple[UsernameCollector, ...] = REGISTERED_USERNAME_COLLECTORS,
) -> list[UsernameResult]:
    """Consulta um username em todas as fontes registradas."""

    return [
        collector(username)
        for collector in collectors
    ]
