"""Interface de linha de comando."""

from osint_local.version import (
    APP_NAME,
    AUTHOR,
    DESCRIPTION,
    VERSION,
)


def main() -> None:
    """Ponto de entrada da aplicação."""

    print("=" * 50)
    print(APP_NAME)
    print("=" * 50)
    print()

    print(f"Versão : {VERSION}")
    print(f"Autor  : {AUTHOR}")
    print()

    print(DESCRIPTION)
