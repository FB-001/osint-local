"""Apresentação dos resultados da pesquisa de usernames."""

from osint_local.models.username_result import (
    UsernameResult,
    UsernameStatus,
)

from osint_local.ui.console import (
    format_field,
    format_footer,
    format_header,
    format_paragraph,
    format_section,
)

from osint_local.ui.formatters import (
    format_success,
    format_warning,
)


def format_username_results(
    username: str,
    results: list[UsernameResult],
) -> str:
    """Retorna um relatório consolidado da pesquisa."""

    confirmed = sum(
        result.status == UsernameStatus.CONFIRMED
        for result in results
    )

    absent = sum(
        result.status == UsernameStatus.ABSENT
        for result in results
    )

    blocked = sum(
        result.status == UsernameStatus.BLOCKED
        for result in results
    )

    inconclusive = sum(
        result.status == UsernameStatus.INCONCLUSIVE
        for result in results
    )

    error = sum(
        result.status == UsernameStatus.ERROR
        for result in results
    )

    lines = [
        format_header("Pesquisa de identificador"),
        "",
        format_section("Identificador"),
        "",
        format_field("Username", username),
        "",
        format_section("Resultados"),
        "",
    ]

    for result in results:

        lines.append(result.platform)

        lines.append(
            format_field(
                "Status",
                result.status.value.capitalize(),
            )
        )

        if result.status_code is not None:
            lines.append(
                format_field(
                    "HTTP",
                    str(result.status_code),
                )
            )

        if result.profile_url:
            lines.append(
                format_field(
                    "URL",
                    result.profile_url,
                )
            )

        if result.status == UsernameStatus.CONFIRMED:
            lines.append(
                format_success(
                    "Perfil confirmado."
                )
            )

        elif result.status == UsernameStatus.ABSENT:
            lines.append(
                format_warning(
                    "Nenhum perfil encontrado."
                )
            )

        elif result.status == UsernameStatus.BLOCKED:
            lines.append(
                format_warning(
                    "Consulta bloqueada pela plataforma."
                )
            )

        elif result.status == UsernameStatus.INCONCLUSIVE:
            lines.append(
                format_warning(
                    "Resultado inconclusivo."
                )
            )

        elif result.status == UsernameStatus.ERROR:
            lines.append(
                format_warning(
                    "Erro durante a consulta."
                )
            )

        lines.append("")

    lines.extend(
        [
            format_section("Resumo"),
            "",
            format_field("Fontes", str(len(results))),
            format_field("Confirmadas", str(confirmed)),
            format_field("Ausentes", str(absent)),
            format_field("Bloqueadas", str(blocked)),
            format_field("Inconclusivas", str(inconclusive)),
            format_field("Erros", str(error)),
            "",
            format_paragraph(
                "A existência do mesmo identificador em uma plataforma "
                "não comprova, isoladamente, vínculo com o alvo "
                "investigado."
            ),
            "",
            format_footer(),
        ]
    )

    return "\n".join(lines)
