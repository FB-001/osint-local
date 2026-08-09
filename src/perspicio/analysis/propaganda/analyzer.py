"""Análise inicial de arquivos de propaganda."""

from pathlib import Path

from PIL import Image, UnidentifiedImageError

from perspicio.analysis.propaganda.analysis import PropagandaAnalysis
from perspicio.analysis.propaganda.observations import PropagandaObservations
from perspicio.analysis.propaganda.ocr import (
    extract_text_with_confidence,
    filter_ocr_by_confidence,
)
from perspicio.analysis.propaganda.vision.colors import extract_dominant_colors
from perspicio.analysis.propaganda.vision.yolo import detect_visual_elements


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

    ocr_results = extract_text_with_confidence(file_path)

    raw_texts = [
        result.text
        for result in ocr_results
    ]

    texts = filter_ocr_by_confidence(ocr_results)

    colors = extract_dominant_colors(file_path)

    visual_elements = detect_visual_elements(file_path)

    return PropagandaAnalysis(
        identification=file_path.name,
        observed=PropagandaObservations(
            raw_texts=raw_texts,
            texts=texts,
            colors=colors,
            visual_elements=visual_elements,
        ),
    )
