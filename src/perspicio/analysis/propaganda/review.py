"""Revisão e validação de sugestões de análise de propaganda."""

import typer

from perspicio.analysis.propaganda.analysis import PropagandaAnalysis
from perspicio.analysis.propaganda.ocr import (
    OcrText,
    OcrTextStatus,
)
from perspicio.analysis.propaganda.vision.detections import (
    DetectionStatus,
    VisualDetection,
)
from perspicio.analysis.propaganda.vision.draft import PropagandaAnalysisDraft
from perspicio.analysis.propaganda.vision.labels import translate_yolo_label


def review_ocr_texts(
    texts: list[OcrText],
) -> list[str]:
    """Solicita ao operador a revisão dos textos identificados pelo OCR."""

    if not texts:
        return []

    print()
    print("REVISÃO DOS TEXTOS IDENTIFICADOS")
    print()

    final_texts = []

    for item in texts:
        print(
            f'Texto: "{item.text}" '
            f"({item.confidence:.2f}%)"
        )

        while True:
            action = typer.prompt(
                "[A] Aceitar  [C] Corrigir  [R] Rejeitar",
                default="A",
            ).strip().lower()

            if action == "a":
                item.status = OcrTextStatus.VALIDATED
                final_texts.append(item.text)
                break

            if action == "c":
                corrected = typer.prompt(
                    "Texto correto"
                ).strip()

                if not corrected:
                    print(
                        "O texto corrigido não pode ficar vazio."
                    )
                    continue

                item.corrected_text = corrected
                item.status = OcrTextStatus.CORRECTED
                final_texts.append(item.final_text)
                break

            if action == "r":
                item.status = OcrTextStatus.REJECTED
                break

            print(
                "Opção inválida. Informe A, C ou R."
            )

        print()

    return final_texts


def review_visual_elements(
    detections: list[VisualDetection],
) -> None:
    """Solicita ao operador a validação das detecções visuais."""

    if not detections:
        return

    print()
    print("REVISÃO DOS ELEMENTOS VISUAIS")
    print()

    for detection in detections:
        label = translate_yolo_label(detection.label)
        confidence = detection.confidence * 100

        confirmed = typer.confirm(
            f'Confirmar "{label}" ({confidence:.2f}%)?',
            default=True,
        )

        detection.status = (
            DetectionStatus.VALIDATED
            if confirmed
            else DetectionStatus.REJECTED
        )


def apply_validated_draft(
    analysis: PropagandaAnalysis,
    draft: PropagandaAnalysisDraft,
) -> PropagandaAnalysis:
    """Aplica à análise final somente sugestões validadas pelo operador."""

    if draft.propaganda_type and draft.propaganda_type.validated:
        analysis.propaganda_type = draft.propaganda_type.value

    if draft.classification and draft.classification.validated:
        analysis.classification = draft.classification.value

    if draft.credibility and draft.credibility.validated:
        analysis.credibility = draft.credibility.value

    if draft.coherence and draft.coherence.validated:
        analysis.coherence = draft.coherence.value

    if draft.significance and draft.significance.validated:
        analysis.significance = draft.significance.value

    if draft.positivity and draft.positivity.validated:
        analysis.positivity = draft.positivity.value

    if draft.permanence and draft.permanence.validated:
        analysis.permanence = draft.permanence.value

    if draft.adequacy and draft.adequacy.validated:
        analysis.adequacy = draft.adequacy.value

    if draft.opportunity and draft.opportunity.validated:
        analysis.opportunity = draft.opportunity.value

    if draft.force_idea and draft.force_idea.validated:
        analysis.force_idea = draft.force_idea.value

    if draft.theme and draft.theme.validated:
        analysis.theme = draft.theme.value

    if draft.slogan and draft.slogan.validated:
        analysis.slogan = draft.slogan.value

    if draft.symbol and draft.symbol.validated:
        analysis.symbol = draft.symbol.value

    if draft.origin and draft.origin.validated:
        analysis.ocave.origin = draft.origin.value

    if draft.content and draft.content.validated:
        analysis.ocave.content = draft.content.value

    if draft.target_audience and draft.target_audience.validated:
        analysis.ocave.target_audience = draft.target_audience.value

    if draft.vehicle and draft.vehicle.validated:
        analysis.ocave.vehicle = draft.vehicle.value

    if draft.effect and draft.effect.validated:
        analysis.ocave.effect = draft.effect.value

    return analysis
