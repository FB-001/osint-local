"""Extração local de texto de peças de propaganda."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import subprocess


class OcrTextStatus(str, Enum):
    """Estados possíveis de um texto identificado pelo OCR."""

    PENDING = "pending"
    VALIDATED = "validated"
    CORRECTED = "corrected"
    REJECTED = "rejected"


@dataclass
class OcrText:
    """Representa um texto identificado pelo OCR."""

    text: str
    confidence: float
    status: OcrTextStatus = OcrTextStatus.PENDING
    corrected_text: str | None = None

    @property
    def final_text(self) -> str:
        """Retorna o texto corrigido, quando houver, ou o original."""

        if self.corrected_text:
            return self.corrected_text

        return self.text


def extract_text_with_confidence(
    file_path: Path,
    language: str = "por",
) -> list[OcrText]:
    """Extrai textos e suas confianças utilizando Tesseract OCR."""

    result = subprocess.run(
        [
            "tesseract",
            str(file_path),
            "stdout",
            "-l",
            language,
            "tsv",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    texts = []

    lines = result.stdout.splitlines()

    for line in lines[1:]:
        columns = line.split("\t")

        if len(columns) < 12:
            continue

        text = columns[11].strip()

        if not text:
            continue

        try:
            confidence = float(columns[10])
        except ValueError:
            continue

        if confidence < 0:
            continue

        texts.append(
            OcrText(
                text=text,
                confidence=confidence,
            )
        )

    return texts


def filter_ocr_by_confidence(
    results: list[OcrText],
    minimum_confidence: float = 80.0,
) -> list[str]:
    """Seleciona textos de OCR com confiança mínima."""

    texts = []

    for result in results:
        text = result.text.strip()

        if not text:
            continue

        if result.confidence < minimum_confidence:
            continue

        texts.append(text)

    return texts


def select_ocr_by_confidence(
    results: list[OcrText],
    minimum_confidence: float = 80.0,
) -> list[OcrText]:
    """Seleciona resultados de OCR preservando confiança e estado."""

    return [
        result
        for result in results
        if (
            result.text.strip()
            and result.confidence >= minimum_confidence
        )
    ]
