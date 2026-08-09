"""Coleta de informações técnicas e metadados EXIF de imagens."""

from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from PIL import ExifTags, Image, UnidentifiedImageError

from perspicio.models.photo_metadata import PhotoMetadata
from perspicio.errors import (
    ImageFileNotFoundError,
    ImagePermissionError,
    InvalidImageError,
)


GPS_INFO_TAG = 34853


def calculate_sha256(file_path: Path) -> str:
    """Calcula o hash SHA-256 de um arquivo."""

    file_hash = sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(8192):
            file_hash.update(chunk)

    return file_hash.hexdigest()


def convert_to_decimal(
    coordinates: tuple[Any, Any, Any],
    reference: str,
) -> float:
    """Converte coordenadas EXIF de graus, minutos e segundos para decimal."""

    degrees = float(coordinates[0])
    minutes = float(coordinates[1])
    seconds = float(coordinates[2])

    decimal = degrees + minutes / 60 + seconds / 3600

    if reference in {"S", "W"}:
        decimal *= -1

    return decimal


def extract_gps(exif: Any) -> tuple[float | None, float | None]:
    """Extrai latitude e longitude dos metadados EXIF."""

    gps_data = exif.get_ifd(GPS_INFO_TAG)

    if not gps_data:
        return None, None

    decoded_gps = {
        ExifTags.GPSTAGS.get(tag, tag): value
        for tag, value in gps_data.items()
    }

    latitude_data = decoded_gps.get("GPSLatitude")
    latitude_reference = decoded_gps.get("GPSLatitudeRef")
    longitude_data = decoded_gps.get("GPSLongitude")
    longitude_reference = decoded_gps.get("GPSLongitudeRef")

    if not all(
        [
            latitude_data,
            latitude_reference,
            longitude_data,
            longitude_reference,
        ]
    ):
        return None, None

    latitude = convert_to_decimal(
        latitude_data,
        latitude_reference,
    )
    longitude = convert_to_decimal(
        longitude_data,
        longitude_reference,
    )

    return latitude, longitude


def extract_capture_datetime(exif_data: dict[str, Any]) -> datetime | None:
    """Converte a data EXIF da captura em um objeto datetime."""

    date_text = (
        exif_data.get("DateTimeOriginal")
        or exif_data.get("DateTimeDigitized")
        or exif_data.get("DateTime")
    )

    if not date_text:
        return None

    try:
        return datetime.strptime(date_text, "%Y:%m:%d %H:%M:%S")
    except (TypeError, ValueError):
        return None


def analyze_image(file_path: str | Path) -> PhotoMetadata:
    """Analisa uma imagem local e retorna seus metadados técnicos."""

    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise ImageFileNotFoundError(path)

    if not path.is_file():
        raise InvalidImageError(path)

    try:
        with Image.open(path) as image:
            width, height = image.size
            exif = image.getexif()

            exif_data = {
                ExifTags.TAGS.get(tag, tag): value
                for tag, value in exif.items()
            }

            device_model = exif_data.get("Model")
            captured_at = extract_capture_datetime(exif_data)
            latitude, longitude = extract_gps(exif)

    except PermissionError as error:
        raise ImagePermissionError(path) from error

    except UnidentifiedImageError as error:
        raise InvalidImageError(path) from error

    return PhotoMetadata(
        file_path=path,
        device_model=device_model,
        captured_at=captured_at,
        latitude=latitude,
        longitude=longitude,
        width=width,
        height=height,
        file_size_bytes=path.stat().st_size,
        sha256=calculate_sha256(path),
    )
