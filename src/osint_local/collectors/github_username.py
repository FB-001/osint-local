"""Consulta pública de nomes de usuário no GitHub."""

from time import perf_counter
from urllib.parse import quote

import httpx

from osint_local.models.username_result import (
    UsernameResult,
    UsernameStatus,
)


GITHUB_API_URL = "https://api.github.com/users/{username}"
GITHUB_PROFILE_URL = "https://github.com/{username}"

REQUEST_HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "osint-local/0.1.0",
    "X-GitHub-Api-Version": "2022-11-28",
}


def search_github_username(username: str) -> UsernameResult:
    """Verifica publicamente a existência de um usuário no GitHub."""

    normalized_username = username.strip()

    if not normalized_username:
        return UsernameResult(
            username=username,
            platform="GitHub",
            profile_url="",
            status=UsernameStatus.ERROR,
            notes="O nome de usuário está vazio.",
        )

    encoded_username = quote(normalized_username, safe="")
    api_url = GITHUB_API_URL.format(username=encoded_username)
    profile_url = GITHUB_PROFILE_URL.format(username=encoded_username)

    started_at = perf_counter()

    try:
        response = httpx.get(
            api_url,
            headers=REQUEST_HEADERS,
            timeout=10.0,
            follow_redirects=True,
        )

    except httpx.TimeoutException:
        return UsernameResult(
            username=normalized_username,
            platform="GitHub",
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
            platform="GitHub",
            profile_url=profile_url,
            status=UsernameStatus.ERROR,
            response_time_ms=(perf_counter() - started_at) * 1000,
            evidence=[
                "Ocorreu uma falha durante a comunicação com o GitHub.",
            ],
            notes=str(error),
        )

    response_time_ms = (perf_counter() - started_at) * 1000

    if response.status_code == 200:
        data = response.json()
        returned_login = data.get("login")

        evidence = [
            "A API oficial do GitHub respondeu com HTTP 200.",
        ]

        if returned_login:
            evidence.append(
                f"A API retornou o identificador: {returned_login}."
            )

        return UsernameResult(
            username=normalized_username,
            platform="GitHub",
            profile_url=data.get("html_url", profile_url),
            status=UsernameStatus.CONFIRMED,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            evidence=evidence,
        )

    if response.status_code == 404:
        return UsernameResult(
            username=normalized_username,
            platform="GitHub",
            profile_url=profile_url,
            status=UsernameStatus.ABSENT,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            evidence=[
                "A API oficial do GitHub respondeu com HTTP 404.",
                "Nenhum perfil público foi localizado para o identificador.",
            ],
        )

    if response.status_code in {401, 403, 429}:
        return UsernameResult(
            username=normalized_username,
            platform="GitHub",
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
        platform="GitHub",
        profile_url=profile_url,
        status=UsernameStatus.INCONCLUSIVE,
        status_code=response.status_code,
        response_time_ms=response_time_ms,
        evidence=[
            f"A API respondeu com HTTP {response.status_code}.",
            "O código recebido não permite confirmar nem descartar o perfil.",
        ],
    )
