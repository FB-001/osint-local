from osint_local.collectors.github_username import (
    search_github_username,
)


result = search_github_username("exmplo2026")

print(f"Plataforma: {result.platform}")
print(f"Username: {result.username}")
print(f"Estado: {result.status.value}")
print(f"HTTP: {result.status_code}")
print(f"URL: {result.profile_url}")
print(f"Tempo: {result.response_time_ms:.2f} ms")
print()

print("Evidências:")

for evidence in result.evidence:
    print(f"- {evidence}")

if result.notes:
    print()
    print(f"Observações: {result.notes}")
