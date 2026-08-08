"""Apresentação dos resultados de consulta de empresa."""

from osint_local.models.company_result import CompanyResult
from osint_local.ui.console import (
    format_field,
    format_footer,
    format_header,
    format_paragraph,
    format_section,
)


def format_cnpj(cnpj: str) -> str:
    """Formata um CNPJ com pontuação."""

    digits = "".join(
        character
        for character in cnpj
        if character.isdigit()
    )

    if len(digits) != 14:
        return cnpj

    return (
        f"{digits[0:2]}."
        f"{digits[2:5]}."
        f"{digits[5:8]}/"
        f"{digits[8:12]}-"
        f"{digits[12:14]}"
    )


def format_company_result(company: CompanyResult) -> str:
    """Retorna um relatório textual de consulta de empresa."""

    lines = [
        format_header("Consulta de empresa"),
        "",
        format_section("Identificação"),
        "",
        format_field(
            "CNPJ",
            format_cnpj(company.cnpj),
        ),
        format_field(
            "Razão social",
            company.corporate_name,
        ),
    ]

    if company.trade_name:
        lines.append(
            format_field(
                "Nome fantasia",
                company.trade_name,
            )
        )

    lines.extend(
        [
            format_field(
                "Situação",
                company.status,
            ),
            "",
            format_section("Dados cadastrais"),
            "",
        ]
    )

    if company.legal_nature:
        lines.append(
            format_field(
                "Natureza jurídica",
                company.legal_nature,
            )
        )

    if company.main_activity:
        lines.append(
            format_field(
                "Atividade principal",
                company.main_activity,
            )
        )

    if company.address:
        lines.append(
            format_field(
                "Endereço",
                company.address,
            )
        )

    if company.city or company.state:
        location_parts = [
            part
            for part in (
                company.city,
                company.state,
            )
            if part
        ]

        lines.append(
            format_field(
                "Cidade/UF",
                " / ".join(location_parts),
            )
        )

    if company.partners:
        lines.extend(
            [
                "",
                format_section("Quadro societário"),
                "",
            ]
        )

        for partner in company.partners:
            lines.append(
                format_field(
                    "Nome",
                    partner.name,
                )
            )

            if partner.qualification:
                lines.append(
                    format_field(
                        "Qualificação",
                        partner.qualification,
                    )
                )

            if partner.document:
                lines.append(
                    format_field(
                        "Documento",
                        partner.document,
                    )
                )

            lines.append("")

    lines.extend(
        [
            "",
            format_section("Fonte"),
            "",
            format_field(
                "Fonte",
                company.source,
            ),
            format_field(
                "Consulta",
                company.source_url,
            ),
            "",
            format_section("Observação legal"),
            "",
            format_paragraph(
                "As informações apresentadas foram obtidas "
                "de fontes públicas ou de consultas legalmente "
                "autorizadas. O tratamento desses dados deve "
                "observar a Lei nº 13.709/2018 (LGPD), "
                "especialmente os princípios previstos no art. 6º."
            ),
            "",
            format_footer(),
        ]
    )

    return "\n".join(lines)
