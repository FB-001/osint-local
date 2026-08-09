"""Resultado de uma consulta de empresa."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class CompanyPartner:
    """Representa um integrante do quadro societário."""

    name: str
    qualification: Optional[str] = None
    document: Optional[str] = None


@dataclass(slots=True)
class CompanySecondaryActivity:
    """Representa uma atividade econômica secundária."""

    code: Optional[str] = None
    description: Optional[str] = None


@dataclass(slots=True)
class CompanyResult:
    """Representa o resultado de uma consulta pública de empresa."""

    cnpj: str
    corporate_name: str
    trade_name: str | None
    status: str

    address: str | None
    city: str | None
    state: str | None

    legal_nature: str | None
    main_activity: str | None

    capital_social: float | None = None
    company_size: str | None = None
    activity_start_date: str | None = None

    phone_1: str | None = None
    phone_2: str | None = None
    email: str | None = None

    secondary_activities: list[CompanySecondaryActivity] = field(
        default_factory=list
    )

    source: str = ""
    source_url: str = ""

    partners: list[CompanyPartner] = field(default_factory=list)

    checked_at: datetime = field(default_factory=datetime.now)

    evidence: list[str] = field(default_factory=list)

    notes: str | None = None
