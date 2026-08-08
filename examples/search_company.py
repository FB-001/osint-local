from osint_local.collectors.company.brasilapi import (
    search_company_by_cnpj,
)
from osint_local.presenters.company_summary import (
    format_company_result,
)


company = search_company_by_cnpj(
    "60701190000104"
)

print(format_company_result(company))
