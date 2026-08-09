"""Consulta pública de CNPJ utilizando a BrasilAPI."""

import re
from time import perf_counter

import httpx

from perspicio.errors import (
    CompanyNetworkError,
    CompanyNotFoundError,
    CompanyServiceError,
)
from perspicio.models.company_result import (
    CompanyPartner,
    CompanyResult,
    CompanySecondaryActivity,
)

BRASIL_API_CNPJ_URL = (
    "https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
)

REQUEST_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "perspicio/0.1.0",
}


def normalize_cnpj(cnpj: str) -> str:
    """Remove caracteres que não sejam números."""

    return re.sub(r"\D", "", cnpj)


def search_company_by_cnpj(cnpj: str) -> CompanyResult:
    """Consulta uma empresa pública pelo CNPJ."""

    normalized_cnpj = normalize_cnpj(cnpj)

    if len(normalized_cnpj) != 14:
        raise ValueError("O CNPJ deve possuir 14 dígitos.")

    url = BRASIL_API_CNPJ_URL.format(
        cnpj=normalized_cnpj,
    )

    started_at = perf_counter()

    try:
        response = httpx.get(
            url,
            headers=REQUEST_HEADERS,
            timeout=10.0,
            follow_redirects=True,
        )

    except httpx.TimeoutException as error:
        raise CompanyNetworkError(
            "A consulta excedeu o tempo limite."
        ) from error

    except httpx.RequestError as error:
        raise CompanyNetworkError(
            "Não foi possível acessar a fonte de consulta."
        ) from error

    if response.status_code == 404:
        raise CompanyNotFoundError(
            "O CNPJ não foi localizado."
        )

    if response.status_code != 200:
        raise CompanyServiceError(
            f"A fonte respondeu com HTTP {response.status_code}."
        )

    try:
        data = response.json()

    except ValueError as error:
        raise CompanyServiceError(
            "A fonte retornou uma resposta inválida."
        ) from error

    partners: list[CompanyPartner] = []

    for partner in data.get("qsa", []):
        partners.append(
            CompanyPartner(
                name=partner.get(
                    "nome_socio",
                    "Não informado",
                ),
                qualification=partner.get(
                    "qualificacao_socio",
                ),
                document=partner.get(
                    "cnpj_cpf_do_socio",
                ),
            )
        )

    secondary_activities: list[CompanySecondaryActivity] = []

    for activity in data.get("cnaes_secundarios", []):
        secondary_activities.append(
            CompanySecondaryActivity(
                code=str(
                    activity.get("codigo")
                )
                if activity.get("codigo") is not None
                else None,
                description=activity.get(
                    "descricao",
                ),
            )
        )

    address_parts = [
        data.get("descricao_tipo_de_logradouro"),
        data.get("logradouro"),
        data.get("numero"),
        data.get("complemento"),
        data.get("bairro"),
    ]

    address = ", ".join(
        str(part).strip()
        for part in address_parts
        if part
    )

    evidence = [
        "Consulta pública realizada por CNPJ.",
        (
            "Resposta recebida em "
            f"{(perf_counter() - started_at) * 1000:.2f} ms."
        ),
    ]

    return CompanyResult(
        cnpj=data.get(
            "cnpj",
            normalized_cnpj,
        ),
        corporate_name=data.get(
            "razao_social",
            "não informado",
        ),
        trade_name=data.get(
            "nome_fantasia",
        ),
        status=data.get(
            "descricao_situacao_cadastral",
            "não informado",
        ),
        address=address or None,
        city=data.get(
            "municipio",
        ),
        state=data.get(
            "uf",
        ),
        legal_nature=data.get(
            "natureza_juridica",
        ),
        main_activity=data.get(
            "cnae_fiscal_descricao",
        ),
        capital_social=data.get(
            "capital_social",
        ),
        company_size=(
            data.get("descricao_porte")
            or data.get("porte")
        ),
        activity_start_date=data.get(
            "data_inicio_atividade",
        ),
        phone_1=(
            data.get("ddd_telefone_1")
            or data.get("ddd_telefone1")
        ),
        phone_2=(
            data.get("ddd_telefone_2")
            or data.get("ddd_telefone2")
        ),
        email=data.get(
            "email",
        ),
        secondary_activities=secondary_activities,
        source="BrasilAPI",
        source_url=url,
        partners=partners,
        evidence=evidence,
    )
