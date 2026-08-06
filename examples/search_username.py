from osint_local.analyzers.username_search import search_username


results = search_username("FB-001")

for result in results:
    print(f"Plataforma: {result.platform}")
    print(f"Estado: {result.status.value}")
    print(f"URL: {result.profile_url}")
    print()
