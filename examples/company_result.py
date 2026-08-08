from osint_local.models.company_result import CompanyResult

company = CompanyResult(
    cnpj="12.345.678/0001-90",
    corporate_name="Empresa Exemplo Ltda.",
    trade_name="Empresa Exemplo",
    status="Ativa",
    address="Rua Exemplo, 100",
    city="Rio de Janeiro",
    state="RJ",
    legal_nature="Sociedade Empresária Limitada",
    main_activity="Desenvolvimento de Software",
    source="Fonte pública de teste",
    source_url="https://exemplo.gov.br",
)

print(company)
