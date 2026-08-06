"""Consulta exata de contas Mastodon por identificador federado."""

from time import perf_counter

import httpx

from osint_local.models.username_result import (
    UsernameResult,
    UsernameStatus,
)


REQUEST_HEADERS = {
    "Accept": "application/jrd+json, application/json",
    "User-Agent": "osint-local/0.1.0",
}


def normalize_mastodon_handle(handle: str) -> tuple[str, str] | None:
    """Separa um identificador Mastodon em usuário e instância."""

    normalized_handle = handle.strip().lstrip("@")

    if normalized_handle.count("@") != 1:
        return None

    username, instance = normalized_handle.split("@", maxsplit=1)

    if not username or not instance:
        return None

    if "." not in instance or "/" in instance or ":" in instance:
        return None

    return username, instance.lower()


def search_mastodon_username(handle: str) -> UsernameResult:
    """Verifica uma conta Mastodon por meio do WebFinger."""

    normalized = normalize_mastodon_handle(handle)

    if normalized is None:
        return UsernameResult(
            username=handle.strip(),
            platform="Mastodon",
            profile_url="",
            status=UsernameStatus.ERROR,
            evidence=[
                "O identificador não contém usuário e instância válidos.",
            ],
            notes=(
                "Use o formato usuario@instancia, por exemplo: "
                "gargron@mastodon.social."
            ),
        )

    username, instance = normalized
    account = f"{username}@{instance}"
    webfinger_url = f"https://{instance}/.well-known/webfinger"
    profile_url = f"https://{instance}/@{username}"

    started_at = perf_counter()

    try:
        response = httpx.get(
            webfinger_url,
            params={"resource": f"acct:{account}"},
            headers=REQUEST_HEADERS,
            timeout=10.0,
            follow_redirects=True,
        )

    except httpx.TimeoutException:
        return UsernameResult(
            username=account,
            platform="Mastodon",
            profile_url=profile_url,
            status=UsernameStatus.INCONCLUSIVE,
            response_time_ms=(perf_counter() - started_at) * 1000,
            evidence=[
                "A instância não respondeu dentro do tempo limite.",
            ],
            notes="Não foi possível concluir a verificação.",
        )

    except httpx.RequestError as error:
        return UsernameResult(
            username=account,
            platform="Mastodon",
            profile_url=profile_url,
            status=UsernameStatus.ERROR,
            response_time_ms=(perf_counter() - started_at) * 1000,
            evidence=[
                "Ocorreu uma falha de comunicação com a instância.",
            ],
            notes=str(error),
        )

    response_time_ms = (perf_counter() - started_at) * 1000

    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
            return UsernameResult(
                username=account,
                platform="Mastodon",
                profile_url=profile_url,
                status=UsernameStatus.INCONCLUSIVE,
                status_code=response.status_code,
                response_time_ms=response_time_ms,
                evidence=[
                    "A instância respondeu com HTTP 200.",
                    "A resposta não pôde ser interpretada como JSON.",
                ],
            )

        subject = str(data.get("subject", "")).removeprefix("acct:")
        aliases = data.get("aliases", [])

        if subject.casefold() != account.casefold():
            return UsernameResult(
                username=account,
                platform="Mastodon",
                profile_url=profile_url,
                status=UsernameStatus.INCONCLUSIVE,
                status_code=response.status_code,
                response_time_ms=response_time_ms,
                evidence=[
                    "A instância respondeu com HTTP 200.",
                    "O identificador retornado não corresponde ao consultado.",
                ],
            )

        if aliases:
            profile_url = aliases[0]

        return UsernameResult(
            username=account,
            platform="Mastodon",
            profile_url=profile_url,
            status=UsernameStatus.CONFIRMED,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            evidence=[
                "O endpoint WebFinger respondeu com HTTP 200.",
                f"O identificador retornado corresponde a {subject}.",
            ],
        )

    if response.status_code == 404:
        return UsernameResult(
            username=account,
            platform="Mastodon",
            profile_url=profile_url,
            status=UsernameStatus.ABSENT,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            evidence=[
                "O endpoint WebFinger respondeu com HTTP 404.",
                "A instância não localizou o identificador informado.",
            ],
        )

    if response.status_code in {401, 403, 429}:
        return UsernameResult(
            username=account,
            platform="Mastodon",
            profile_url=profile_url,
            status=UsernameStatus.BLOCKED,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            evidence=[
                f"A instância respondeu com HTTP {response.status_code}.",
                "A consulta foi recusada ou limitada pela instância.",
            ],
        )

    return UsernameResult(
        username=account,
        platform="Mastodon",
        profile_url=profile_url,
        status=UsernameStatus.INCONCLUSIVE,
        status_code=response.status_code,
        response_time_ms=response_time_ms,
        evidence=[
            f"A instância respondeu com HTTP {response.status_code}.",
            "A resposta não permite confirmar nem descartar a conta.",
        ],
    )
