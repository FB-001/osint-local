"""Apresentação legível de uma investigação no terminal."""

from osint_local.models.investigation import Investigation


def format_investigation(case: Investigation) -> str:
    """Retorna um resumo organizado da investigação."""

    lines = [
        "=" * 60,
        f"INVESTIGAÇÃO: {case.name}",
        "=" * 60,
        f"Analista: {case.analyst}",
        f"Status: {case.status}",
        f"Criada em: {case.created_at:%d/%m/%Y %H:%M:%S}",
        "",
        "Descrição:",
        case.description,
        "",
        f"ALVOS ({len(case.targets)})",
        "-" * 60,
    ]

    if not case.targets:
        lines.append("Nenhum alvo cadastrado.")
    else:
        for index, target in enumerate(case.targets, start=1):
            lines.extend(
                [
                    f"{index}. {target.full_name}",
                    f"   CPF: {target.cpf or 'não informado'}",
                    (
                        "   Telefones: "
                        + (
                            ", ".join(target.phone_numbers)
                            if target.phone_numbers
                            else "não informados"
                        )
                    ),
                    (
                        "   E-mails: "
                        + (
                            ", ".join(target.emails)
                            if target.emails
                            else "não informados"
                        )
                    ),
                    (
                        "   Endereços: "
                        + (
                            ", ".join(target.addresses)
                            if target.addresses
                            else "não informados"
                        )
                    ),
                    "",
                ]
            )

    lines.extend(
        [
            f"EVIDÊNCIAS ({len(case.evidences)})",
            "-" * 60,
        ]
    )

    if not case.evidences:
        lines.append("Nenhuma evidência cadastrada.")
    else:
        for index, evidence in enumerate(case.evidences, start=1):
            lines.extend(
                [
                    f"{index}. Tipo: {evidence.evidence_type}",
                    f"   Origem: {evidence.source}",
                    f"   Coletada em: {evidence.collected_at:%d/%m/%Y %H:%M:%S}",
                    f"   Descrição: {evidence.description}",
                    f"   Observações: {evidence.notes or 'nenhuma'}",
                    "",
                ]
            )

    return "\n".join(lines)
