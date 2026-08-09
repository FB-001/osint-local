"""Exceções relacionadas ao cálculo e à comparação de hashes."""

from pathlib import Path

from perspicio.errors.base import OsintLocalError


class HashAnalysisError(OsintLocalError):
    """Erro geral ocorrido durante uma análise de integridade."""


class HashFileNotFoundError(HashAnalysisError):
    """Indica que um arquivo da comparação não foi encontrado."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

        super().__init__(
            f"Arquivo não encontrado para cálculo de hash: {file_path}"
        )


class HashPermissionError(HashAnalysisError):
    """Indica falta de permissão para ler um arquivo."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

        super().__init__(
            f"Sem permissão para calcular o hash: {file_path}"
        )


class HashCalculationError(HashAnalysisError):
    """Indica uma falha inesperada no cálculo do hash."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

        super().__init__(
            f"Não foi possível calcular o hash do arquivo: {file_path}"
        )
