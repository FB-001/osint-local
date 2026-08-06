from osint_local.collectors.gitlab_username import (
    search_gitlab_username,
)


result = search_gitlab_username("gitlab-org")

print(f"Plataforma: {result.platform}")
print(f"Username: {result.username}")
print(f"Estado: {result.status.value}")
print(f"HTTP: {result.status_code}")
print(f"URL: {result.profile_url}")

if result.response_time_ms is not None:
    print(f"Tempo: {result.response_time_ms:.2f} ms")

print()
print("Evidências:")

for evidence in result.evidence:
    print(f"- {evidence}")

if result.notes:
    print()
    print(f"Observações: {result.notes}")
