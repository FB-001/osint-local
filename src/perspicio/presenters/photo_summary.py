"""Apresentação legível dos metadados de uma imagem."""

from perspicio.models.photo_metadata import PhotoMetadata
from perspicio.ui.console import (
    format_field,
    format_footer,
    format_header,
    format_section,
)


def format_photo_metadata(metadata: PhotoMetadata) -> str:
    """Retorna um relatório textual dos metadados da imagem."""

    captured_at = (
        metadata.captured_at.strftime("%d/%m/%Y %H:%M:%S")
        if metadata.captured_at
        else "não informada"
    )

    lines = [
        format_header("Análise de imagem"),
        "",
        format_section("Identificação do arquivo"),
        "",
        format_field("Arquivo", metadata.file_path.name),
        format_field(
            "Tamanho",
            f"{metadata.file_size_bytes} bytes",
        ),
        format_field(
            "Dimensões",
            f"{metadata.width} x {metadata.height}",
        ),
        "",
        format_section("Metadados EXIF"),
        "",
        format_field(
            "Aparelho",
            metadata.device_model or "não informado",
        ),
        format_field("Capturada em", captured_at),
    ]

    if metadata.latitude is not None and metadata.longitude is not None:
        lines.extend(
            [
                format_field(
                    "Latitude",
                    f"{metadata.latitude:.6f}",
                ),
                format_field(
                    "Longitude",
                    f"{metadata.longitude:.6f}",
                ),
            ]
        )
    else:
        lines.append(
            format_field("Localização GPS", "não informada")
        )

    lines.extend(
        [
            "",
            format_section("Integridade"),
            "",
            "SHA-256:",
            metadata.sha256,
            "",
            format_footer(),
        ]
    )

    return "\n".join(lines)
