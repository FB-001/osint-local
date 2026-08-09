"""Modelo de uma empresa encontrada em fonte pública."""

from dataclasses import dataclass


@dataclass(slots=True)
class Company:
    """Representa uma empresa localizada."""

    cnpj: str
    corporate_name: str
    trade_name: str | None
    status: str
    address: str | None
    city: str | None
    state: str | None
    legal_nature: str | None
    main_activity: str | None
