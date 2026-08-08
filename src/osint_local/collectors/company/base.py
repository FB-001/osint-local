"""Interfaces para coletores de empresas."""

from abc import ABC, abstractmethod

from osint_local.models.company import Company


class CompanyCollector(ABC):
    """Classe base para qualquer coletor de empresas."""

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Nome da fonte consultada."""

    @abstractmethod
    def search(self, cnpj: str) -> Company:
        """Consulta uma empresa utilizando um CNPJ."""
