from osint_local.models.username_result import (
    UsernameResult,
    UsernameStatus,
)


result = UsernameResult(
    username="usuario_teste",
    platform="Plataforma de teste",
    profile_url="https://example.com/usuario_teste",
    status=UsernameStatus.CONFIRMED,
    status_code=200,
    response_time_ms=243.7,
    evidence=[
        "Servidor respondeu com HTTP 200.",
        "Nome de usuário encontrado na página.",
    ],
)

print(result)
print()
print(f"Plataforma: {result.platform}")
print(f"Estado: {result.status.value}")
print(f"Evidências: {len(result.evidence)}")
