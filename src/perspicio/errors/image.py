"""Exceções relacionadas à análise de imagens."""

from pathlib import Path

from perspicio.errors.base import OsintLocalError


class ImageAnalysisError(OsintLocalError):
    """Erro geral ocorrido durante a análise de uma imagem."""


class ImageFileNotFoundError(ImageAnalysisError):
    """Indica que o arquivo de imagem não foi encontrado."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

        super().__init__(
            f"Arquivo de imagem não encontrado: {file_path}"
        )


class InvalidImageError(ImageAnalysisError):
    """Indica que o arquivo não é uma imagem reconhecida."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

        super().__init__(
            f"O arquivo não é uma imagem reconhecida: {file_path}"
        )


class ImagePermissionError(ImageAnalysisError):
    """Indica falta de permissão para ler a imagem."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

        super().__init__(
            f"Sem permissão para ler a imagem: {file_path}"
        )
