"""Análise inicial de arquivos de propaganda."""

from pathlib import Path

from PIL import Image, UnidentifiedImageError

from perspicio.analysis.propaganda.analysis import PropagandaAnalysis


SUPPORTED_IMAGE_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def analyze_propaganda(file_path: Path) -> PropagandaAnalysis:
    """Cria uma análise de propaganda a partir de um arquivo."""

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    if not file_path.is_file():
        raise ValueError(
            "O caminho informado não corresponde a um arquivo."
        )

    if file_path.suffix.lower() not in SUPPORTED_IMAGE_FORMATS:
        raise ValueError(
            "Formato de arquivo não suportado para análise de propaganda."
        )

    try:
        with Image.open(file_path) as image:
            image.verify()

    except (UnidentifiedImageError, OSError) as error:
        raise ValueError(
            "O arquivo informado não contém uma imagem válida."
        ) from error

    return PropagandaAnalysis(
        identification=file_path.name,
    )
