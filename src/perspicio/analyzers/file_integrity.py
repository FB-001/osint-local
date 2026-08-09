"""Análise de integridade e identidade de arquivos."""

from pathlib import Path

from perspicio.collectors.image.metadata import calculate_sha256
from perspicio.errors import (
    HashCalculationError,
    HashFileNotFoundError,
    HashPermissionError,
)
from perspicio.models.hash_comparison import HashComparison


def calculate_file_hash(file_path: Path) -> str:
    """Calcula o SHA-256 com tratamento de erros do domínio."""

    try:
        return calculate_sha256(file_path)

    except PermissionError as error:
        raise HashPermissionError(file_path) from error

    except OSError as error:
        raise HashCalculationError(file_path) from error


def compare_files(
    first_file: str | Path,
    second_file: str | Path,
) -> HashComparison:
    """Compara dois arquivos utilizando seus hashes SHA-256."""

    first_path = Path(first_file).expanduser().resolve()
    second_path = Path(second_file).expanduser().resolve()

    for path in (first_path, second_path):
        if not path.exists():
            raise HashFileNotFoundError(path)

        if not path.is_file():
            raise HashCalculationError(path)

    return HashComparison(
        first_file=first_path,
        second_file=second_path,
        first_sha256=calculate_file_hash(first_path),
        second_sha256=calculate_file_hash(second_path),
    )
