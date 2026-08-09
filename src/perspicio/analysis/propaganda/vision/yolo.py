"""Detecção local de elementos visuais utilizando YOLO."""

from pathlib import Path

from ultralytics import YOLO

from perspicio.analysis.propaganda.vision.detections import VisualDetection


def detect_visual_elements(
    file_path: Path,
    model_path: str = "yolo11n.pt",
) -> list[VisualDetection]:
    """Detecta elementos visuais em uma imagem utilizando YOLO."""

    model = YOLO(model_path)

    results = model.predict(
        source=str(file_path),
        device="cpu",
        verbose=False,
    )

    detections = []

    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            class_id = int(box.cls.item())
            confidence = float(box.conf.item())

            label = result.names[class_id]

            detections.append(
                VisualDetection(
                    label=label,
                    confidence=confidence,
                    validated=False,
                )
            )

    return detections
