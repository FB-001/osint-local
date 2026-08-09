"""Erros relacionados à consulta de empresas."""


class CompanyError(Exception):
    """Erro base para consultas de empresa."""


class CompanyNotFoundError(CompanyError):
    """Empresa não localizada."""


class CompanyNetworkError(CompanyError):
    """Falha de comunicação com a fonte."""


class CompanyServiceError(CompanyError):
    """Falha inesperada na fonte consultada."""
