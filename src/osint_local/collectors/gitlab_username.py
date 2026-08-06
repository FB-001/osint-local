"""Consulta pública de nomes de usuário no GitLab."""

from time import perf_counter

import httpx

from osint_local.models.username_result import (
    UsernameResult,
    UsernameStatus,
)


GITLAB_API_URL = "https://gitlab.com/api/v4/users"
GITLAB_PROFILE_URL = "https://gitlab.com/{username}"

REQUEST_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "osint-local/0.1.0",
}


def search_gitlab_username(username: str) -> UsernameResult:
    """Verifica publicamente a existência de um usuário no GitLab."""

    normalized_username = username.strip()
    profile_url = GITLAB_PROFILE_URL.format(
        username=normalized_username
    )

    if not normalized_username:
        return UsernameResult(
            username=username,
            platform="GitLab",
            profile_url="",
            status=UsernameStatus.ERROR,
            notes="O nome de usuário está vazio.",
        )

    started_at = perf_counter()

    try:
        response = httpx.get(
            GITLAB_API_URL,
            params={
                "search": normalized_username,
            },
            headers=REQUEST_HEADERS,
            timeout=10.0,
            follow_redirects=True,
        )

    except httpx.TimeoutException:
        return UsernameResult(
            username=normalized_username,
            platform="GitLab",
            profile_url=profile_url,
            status=UsernameStatus.INCONCLUSIVE,
            response_time_ms=(perf_counter() - started_at) * 1000,
            evidence=[
                "A consulta excedeu o tempo limite configurado.",
            ],
            notes="Não foi possível concluir a verificação.",
        )

    except httpx.RequestError as error:
        return UsernameResult(
            username=normalized_username,
            platform="GitLab",
            profile_url=profile_url,
            status=UsernameStatus.ERROR,
            response_time_ms=(perf_counter() - started_at) * 1000,
            evidence=[
                "Ocorreu uma falha durante a comunicação com o GitLab.",
            ],
            notes=str(error),
        )

    response_time_ms = (perf_counter() - started_at) * 1000

    if response.status_code == 200:
        try:
            users = response.json()
        except ValueError:
            return UsernameResult(
                username=normalized_username,
                platform="GitLab",
                profile_url=profile_url,
                status=UsernameStatus.INCONCLUSIVE,
                status_code=response.status_code,
                response_time_ms=response_time_ms,
                evidence=[
                    "A API respondeu com HTTP 200.",
                    "A resposta não pôde ser interpretada como JSON.",
                ],
            )

        exact_user = next(
            (
                user
                for user in users
                if str(user.get("username", "")).casefold()
                == normalized_username.casefold()
            ),
            None,
        )

        if exact_user is not None:
            returned_username = exact_user.get(
                "username",
                normalized_username,
            )

            evidence = [
                "A API oficial do GitLab respondeu com HTTP 200.",
                (
                    "A resposta contém uma correspondência exata "
                    f"para o identificador: {returned_username}."
                ),
            ]

            state = exact_user.get("state")

            if state:
                evidence.append(
                    f"Estado informado pela plataforma: {state}."
                )

            return UsernameResult(
                username=normalized_username,
                platform="GitLab",
                profile_url=exact_user.get(
                    "web_url",
                    profile_url,
                ),
                status=UsernameStatus.CONFIRMED,
                status_code=response.status_code,
                response_time_ms=response_time_ms,
                evidence=evidence,
            )

        return UsernameResult(
            username=normalized_username,
            platform="GitLab",
            profile_url=profile_url,
            status=UsernameStatus.ABSENT,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            evidence=[
                "A API oficial do GitLab respondeu com HTTP 200.",
                (
                    "Nenhuma correspondência exata foi localizada "
                    "para o identificador."
                ),
            ],
        )

    if response.status_code in {401, 403, 429}:
        return UsernameResult(
            username=normalized_username,
            platform="GitLab",
            profile_url=profile_url,
            status=UsernameStatus.BLOCKED,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            evidence=[
                f"A API respondeu com HTTP {response.status_code}.",
                "A consulta pode ter sido limitada ou bloqueada.",
            ],
            notes="Tente novamente mais tarde.",
        )

    return UsernameResult(
        username=normalized_username,
        platform="GitLab",
        profile_url=profile_url,
        status=UsernameStatus.INCONCLUSIVE,
        status_code=response.status_code,
        response_time_ms=response_time_ms,
        evidence=[
            f"A API respondeu com HTTP {response.status_code}.",
            "O resultado não permite confirmar nem descartar o perfil.",
        ],
    )
