"""Extração de cores predominantes de peças de propaganda."""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class ObservedColor:
    """Representa uma cor predominante observada na imagem."""

    name: str
    rgb: tuple[int, int, int]
    proportion: float


def extract_dominant_colors(
    file_path: Path,
    maximum_colors: int = 5,
) -> list[ObservedColor]:
    """Extrai as cores predominantes e suas proporções aproximadas."""

    with Image.open(file_path) as image:
        image = image.convert("RGB")
        image.thumbnail((200, 200))

        quantized = image.quantize(colors=maximum_colors)
        color_counts = quantized.getcolors()

        if not color_counts:
            return []

        palette = quantized.getpalette()

        if palette is None:
            return []

        total_pixels = sum(count for count, _ in color_counts)
        observed_colors = []

        for count, color_index in color_counts:
            palette_index = color_index * 3

            rgb = (
                palette[palette_index],
                palette[palette_index + 1],
                palette[palette_index + 2],
            )

            proportion = (count / total_pixels) * 100

            observed_colors.append(
                ObservedColor(
                    name=classify_color(rgb),
                    rgb=rgb,
                    proportion=proportion,
                )
            )

        observed_colors.sort(
            key=lambda color: color.proportion,
            reverse=True,
        )

        return observed_colors

def classify_color(rgb: tuple[int, int, int]) -> str:
    """Classifica aproximadamente uma cor RGB por nome."""

    red, green, blue = rgb

    maximum = max(red, green, blue)
    minimum = min(red, green, blue)

    if maximum < 40:
        return "Preto"

    if minimum > 210:
        return "Branco"

    if maximum - minimum < 25:
        if maximum < 100:
            return "Cinza escuro"

        if maximum < 180:
            return "Cinza"

        return "Cinza claro"

    if blue > red and blue > green:
        return "Azul"

    if green > red and green > blue:
        return "Verde"

    if red > green and red > blue:
        if green > 100:
            return "Amarelo"

        return "Vermelho"

    if blue >= red and green >= red:
        return "Azul"

    return "Indeterminada"

def summarize_colors(
    colors: list[ObservedColor],
) -> dict[str, float]:
    """Agrupa cores pelo nome e soma suas proporções."""

    summary: dict[str, float] = {}

    for color in colors:
        summary[color.name] = (
            summary.get(color.name, 0.0)
            + color.proportion
        )

    return summary
