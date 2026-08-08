from osint_local.models.correlation_result import (
    CorrelationResult,
    CorrelationStatus,
)


result = CorrelationResult(
    source="Fonte pública de teste",
    category="Empresa",
    value="Empresa Exemplo Ltda.",
    status=CorrelationStatus.CONFIRMED,
    relationship="Sócio-administrador",
    evidence=[
        "Nome localizado no quadro societário público.",
    ],
)

print(f"Fonte: {result.source}")
print(f"Categoria: {result.category}")
print(f"Valor: {result.value}")
print(f"Estado: {result.status.value}")
print(f"Relação: {result.relationship}")
