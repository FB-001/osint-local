"""Modelo do resultado da comparação entre arquivos."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class HashComparison:
    """Representa a comparação SHA-256 entre dois arquivos."""

    first_file: Path
    second_file: Path
    first_sha256: str
    second_sha256: str

    @property
    def files_are_identical(self) -> bool:
        """Indica se os arquivos possuem conteúdo idêntico."""

        return self.first_sha256 == self.second_sha256
